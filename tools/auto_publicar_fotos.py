import json
import os
import re
import subprocess
import time
from pathlib import Path

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


BASE_DIR = Path(__file__).resolve().parent.parent
FOTOS_DIR = BASE_DIR / "assets" / "fotos"
INDEX_PATH = BASE_DIR / "index.html"

SLEEP_SECONDS = 5
AUTO_SECTION_START = "// AUTO-GENERATED PRODUCT IMAGES START"
AUTO_SECTION_END = "// AUTO-GENERATED PRODUCT IMAGES END"

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
WEBP_EXTS = {".webp"}
ORDER_FILE_NAME = "ordem.txt"
COVER_FILE_NAME = ".capa.txt"

DERIVATIVE_FORMAT = "webp"
DESKTOP_MAX_WIDTH = 1600
MOBILE_MAX_WIDTH = 900


def _run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)


def _git_has_changes() -> bool:
    result = _run(["git", "status", "--porcelain"])
    return bool(result.stdout.strip())


def _git_commit_and_push(message: str) -> None:
    _run(["git", "add", "index.html", str(FOTOS_DIR)])
    if not _git_has_changes():
        return
    _run(["git", "commit", "-m", message])
    _run(["git", "push"])


def _extract_code(folder_name: str) -> str | None:
    if " - " not in folder_name:
        return None
    code = folder_name.split(" - ", 1)[0].strip()
    return code.upper() if code else None


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


def _resize_and_save(src_path: Path, dest_path: Path, max_width: int) -> None:
    if Image is None:
        raise RuntimeError(
            "Pillow não está instalado. Instale com: pip install pillow"
        )
    with Image.open(src_path) as img:
        img_format = img.format or DERIVATIVE_FORMAT
        if str(img_format).upper() == "GIF":
            return
        if img.mode not in ["RGB", "RGBA"]:
            img = img.convert("RGBA" if "A" in img.mode else "RGB")
        width, height = img.size
        if width > max_width:
            new_height = int((max_width / width) * height)
            img = img.resize((max_width, new_height), Image.LANCZOS)
        img.save(
            dest_path,
            DERIVATIVE_FORMAT,
            quality=82,
            method=6,
        )


def _ensure_derivatives(src_path: Path) -> tuple[Path, Path]:
    base = src_path.with_suffix("")
    desktop_path = Path(f"{base}-desktop.{DERIVATIVE_FORMAT}")
    mobile_path = Path(f"{base}-mobile.{DERIVATIVE_FORMAT}")

    if not desktop_path.exists() or desktop_path.stat().st_size == 0:
        _resize_and_save(src_path, desktop_path, DESKTOP_MAX_WIDTH)
    if not mobile_path.exists() or mobile_path.stat().st_size == 0:
        _resize_and_save(src_path, mobile_path, MOBILE_MAX_WIDTH)
    return desktop_path, mobile_path


def _is_derivative_path(path: Path) -> bool:
    name = path.stem.lower()
    return name.endswith("-desktop") or name.endswith("-mobile")


def _iter_product_folders() -> list[Path]:
    folders: list[Path] = []
    if not FOTOS_DIR.exists():
        return folders
    for category in sorted(FOTOS_DIR.iterdir()):
        if not category.is_dir():
            continue
        for folder in sorted(category.iterdir()):
            if folder.is_dir():
                folders.append(folder)
    return folders


def _bootstrap_missing_derivatives() -> bool:
    changed = False
    for folder in _iter_product_folders():
        for img in _sorted_images(folder):
            if img.suffix.lower() not in IMAGE_EXTS:
                continue
            if _is_derivative_path(img):
                continue
            base = img.with_suffix("")
            desktop_path = Path(f"{base}-desktop.{DERIVATIVE_FORMAT}")
            mobile_path = Path(f"{base}-mobile.{DERIVATIVE_FORMAT}")

            needs_desktop = (not desktop_path.exists()) or desktop_path.stat().st_size == 0
            needs_mobile = (not mobile_path.exists()) or mobile_path.stat().st_size == 0
            if not (needs_desktop or needs_mobile):
                continue

            desktop, mobile = _ensure_derivatives(img)
            if desktop.exists() and desktop.stat().st_size > 0:
                changed = True
            if mobile.exists() and mobile.stat().st_size > 0:
                changed = True
    return changed


def _build_mapping() -> dict:
    mapping: dict[str, list[dict]] = {}
    if not FOTOS_DIR.exists():
        return mapping
    for folder in _iter_product_folders():
        code = _extract_code(folder.name)
        if not code:
            continue
        items = []
        cover_item = None
        existing_desktop_paths: set[str] = set()
        cover_file = folder / COVER_FILE_NAME
        cover_base = None
        if cover_file.exists():
            cover_base = cover_file.read_text(encoding="utf-8").strip()
        for img in _sorted_images(folder):
            name = img.name
            if name.endswith("-desktop.webp"):
                if name.startswith("capa-"):
                    continue
                base = name.replace("-desktop.webp", "")
                mobile = folder / f"{base}-mobile.webp"
                full_png = folder / f"{base}.png"
                full_jpg = folder / f"{base}.jpg"
                full = full_png if full_png.exists() else full_jpg if full_jpg.exists() else img
                item = {
                    "desktop": _to_rel(img),
                    "mobile": _to_rel(mobile) if mobile.exists() else _to_rel(img),
                    "full": _to_rel(full),
                }
                if cover_base and base == cover_base:
                    cover_item = item
                else:
                    items.append(item)
                existing_desktop_paths.add(item["desktop"])
        if cover_item:
            items.insert(0, cover_item)

        for img in _sorted_images(folder):
            if img.suffix.lower() not in IMAGE_EXTS:
                continue
            if _is_derivative_path(img):
                continue
            base = img.with_suffix("")
            expected_desktop = Path(f"{base}-desktop.{DERIVATIVE_FORMAT}")
            if expected_desktop.exists() and expected_desktop.name != "capa-desktop.webp":
                if _to_rel(expected_desktop) in existing_desktop_paths:
                    continue
            desktop, mobile = _ensure_derivatives(img)
            items.append(
                {
                    "desktop": _to_rel(desktop if desktop.exists() else img),
                    "mobile": _to_rel(mobile) if mobile.exists() else _to_rel(desktop if desktop.exists() else img),
                    "full": _to_rel(img),
                }
            )
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
    cache_buster = str(int(time.time()))
    new_block = (
        f"{AUTO_SECTION_START}\n"
        f"const IMAGE_CACHE_BUSTER = \"{cache_buster}\";\n"
        f"const productImagesByCode = {mapping_json};\n"
        f"{AUTO_SECTION_END}"
    )

    before = content[:start_idx]
    after = content[end_idx + len(AUTO_SECTION_END):]
    updated = before + new_block + after
    if updated == content:
        return False
    INDEX_PATH.write_text(updated, encoding="utf-8")
    return True


def _snapshot_state() -> str:
    if not FOTOS_DIR.exists():
        return ""
    parts = []
    for folder in _iter_product_folders():
        cover_file = folder / COVER_FILE_NAME
        if cover_file.exists():
            parts.append(f"{cover_file.relative_to(BASE_DIR)}:{cover_file.read_text(encoding='utf-8')}")
        order_file = folder / ORDER_FILE_NAME
        if order_file.exists():
            parts.append(f"{order_file.relative_to(BASE_DIR)}:{order_file.read_text(encoding='utf-8')}")
        for img in _sorted_images(folder):
            parts.append(str(img.relative_to(BASE_DIR)))
    return "|".join(parts)


def main() -> None:
    print("Monitorando assets/fotos... (Ctrl+C para sair)")
    last_state = ""
    while True:
        try:
            _bootstrap_missing_derivatives()
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
