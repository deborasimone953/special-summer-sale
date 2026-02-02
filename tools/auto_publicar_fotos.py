import json
import os
import re
import subprocess
import time
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets" / "fotos" / "Sem categoria"
INDEX_PATH = BASE_DIR / "index.html"

SLEEP_SECONDS = 5
AUTO_SECTION_START = "// AUTO-GENERATED PRODUCT IMAGES START"
AUTO_SECTION_END = "// AUTO-GENERATED PRODUCT IMAGES END"

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
WEBP_EXTS = {".webp"}
ORDER_FILE_NAME = "ordem.txt"


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)


def _git_has_changes() -> bool:
    result = _run(["git", "status", "--porcelain"])
    return bool(result.stdout.strip())


def _git_commit_and_push(message: str) -> None:
    _run(["git", "add", "index.html", str(ASSETS_DIR)])
    if not _git_has_changes():
        return
    _run(["git", "commit", "-m", message])
    _run(["git", "push"])


def _extract_code(folder_name: str) -> str | None:
    match = re.match(r"^\s*([A-Z0-9-]+)\s+-\s+", folder_name, flags=re.IGNORECASE)
    if not match:
        return None
    return match.group(1).upper()


def _load_order(folder: Path) -> list[str]:
    order_file = folder / ORDER_FILE_NAME
    if not order_file.exists():
        return []
    lines = order_file.read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip()]


def _sorted_images(folder: Path) -> list[Path]:
    images = []
    for item in folder.iterdir():
        if not item.is_file():
            continue
        if item.name.startswith("."):
            continue
        if item.suffix.lower() in IMAGE_EXTS or item.suffix.lower() in WEBP_EXTS:
            images.append(item)

    if not images:
        return []

    order = _load_order(folder)
    if not order:
        return sorted(images, key=lambda p: p.name.lower())

    by_name = {img.name: img for img in images}
    ordered = []
    used = set()
    for name in order:
        img = by_name.get(name)
        if img:
            ordered.append(img)
            used.add(name)

    remaining = [img for img in images if img.name not in used]
    return ordered + sorted(remaining, key=lambda p: p.name.lower())


def _build_mapping() -> dict:
    mapping: dict[str, list[dict]] = {}
    if not ASSETS_DIR.exists():
        return mapping
    for folder in sorted(ASSETS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        code = _extract_code(folder.name)
        if not code:
            continue
        items = []
        for img in _sorted_images(folder):
            name = img.name
            if name.endswith("-desktop.webp"):
                base = name.replace("-desktop.webp", "")
                mobile = folder / f"{base}-mobile.webp"
                full_png = folder / f"{base}.png"
                full_jpg = folder / f"{base}.jpg"
                full = full_png if full_png.exists() else full_jpg if full_jpg.exists() else img
                items.append(
                    {
                        "desktop": _to_rel(img),
                        "mobile": _to_rel(mobile) if mobile.exists() else _to_rel(img),
                        "full": _to_rel(full),
                    }
                )
        if items:
            mapping[code] = items
            continue
        for img in _sorted_images(folder):
            if img.suffix.lower() in IMAGE_EXTS:
                items.append({"desktop": _to_rel(img)})
        if items:
            mapping[code] = items
    return mapping


def _to_rel(path: Path) -> str:
    return str(path.relative_to(BASE_DIR)).replace("\\", "/")


def _update_index(mapping: dict) -> bool:
    if not INDEX_PATH.exists():
        return False
    content = INDEX_PATH.read_text(encoding="utf-8")
    start_idx = content.find(AUTO_SECTION_START)
    end_idx = content.find(AUTO_SECTION_END)
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        return False

    mapping_json = json.dumps(mapping, ensure_ascii=False, indent=2)
    new_block = f"{AUTO_SECTION_START}\nconst productImagesByCode = {mapping_json};\n{AUTO_SECTION_END}"

    before = content[:start_idx]
    after = content[end_idx + len(AUTO_SECTION_END):]
    updated = before + new_block + after
    if updated == content:
        return False
    INDEX_PATH.write_text(updated, encoding="utf-8")
    return True


def _snapshot_state() -> str:
    if not ASSETS_DIR.exists():
        return ""
    parts = []
    for folder in sorted(ASSETS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        order_file = folder / ORDER_FILE_NAME
        if order_file.exists():
            parts.append(f"{order_file.relative_to(BASE_DIR)}:{order_file.read_text(encoding='utf-8')}")
        for img in _sorted_images(folder):
            parts.append(str(img.relative_to(BASE_DIR)))
    return "|".join(parts)


def main() -> None:
    print("Monitorando assets/fotos/Sem categoria... (Ctrl+C para sair)")
    last_state = ""
    while True:
        try:
            current_state = _snapshot_state()
            if current_state != last_state:
                mapping = _build_mapping()
                updated = _update_index(mapping)
                if updated:
                    _git_commit_and_push("Atualiza imagens automaticamente.")
                    print("Publicado automaticamente.")
                last_state = current_state
        except Exception as exc:
            print(f"Erro: {exc}")
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
