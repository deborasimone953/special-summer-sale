import os
from pathlib import Path

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None

BASE_DIR = Path(__file__).resolve().parent.parent
SEM_CATEGORIA_DIR = BASE_DIR / "assets" / "fotos" / "Sem categoria"

IMAGE_EXTS = {".jpg", ".jpeg", ".png"}
DERIVATIVE_FORMAT = "webp"
DESKTOP_MAX_WIDTH = 1600
MOBILE_MAX_WIDTH = 900


def _resize_and_save(src_path: Path, dest_path: Path, max_width: int) -> None:
    if Image is None:
        raise RuntimeError("Pillow não está instalado. Instale com: pip install pillow")
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
        img.save(dest_path, DERIVATIVE_FORMAT, quality=82, method=6)


def _ensure_derivatives(src_path: Path) -> tuple[Path, Path, bool]:
    base = src_path.with_suffix("")
    desktop_path = Path(f"{base}-desktop.{DERIVATIVE_FORMAT}")
    mobile_path = Path(f"{base}-mobile.{DERIVATIVE_FORMAT}")

    changed = False
    if (not desktop_path.exists()) or desktop_path.stat().st_size == 0:
        _resize_and_save(src_path, desktop_path, DESKTOP_MAX_WIDTH)
        changed = True
    if (not mobile_path.exists()) or mobile_path.stat().st_size == 0:
        _resize_and_save(src_path, mobile_path, MOBILE_MAX_WIDTH)
        changed = True
    return desktop_path, mobile_path, changed


def main() -> None:
    if not SEM_CATEGORIA_DIR.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {SEM_CATEGORIA_DIR}")

    generated = 0
    scanned = 0

    for product_dir in sorted(SEM_CATEGORIA_DIR.iterdir()):
        if not product_dir.is_dir():
            continue
        for entry in sorted(product_dir.iterdir()):
            if not entry.is_file():
                continue
            if entry.name.startswith("."):
                continue
            if entry.suffix.lower() not in IMAGE_EXTS:
                continue
            stem = entry.stem.lower()
            if stem.endswith("-desktop") or stem.endswith("-mobile"):
                continue
            scanned += 1
            _d, _m, changed = _ensure_derivatives(entry)
            if changed:
                generated += 1

    print(f"Arquivos originais verificados: {scanned}")
    print(f"Derivados gerados/recuperados: {generated}")


if __name__ == "__main__":
    main()
