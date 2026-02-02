import os
from pathlib import Path

from PIL import Image, ImageEnhance
from rembg import remove


BASE_DIR = Path(__file__).resolve().parent.parent
ENTRADA_DIR = BASE_DIR / "assets" / "lote_fundo" / "entrada"
SAIDA_DIR = BASE_DIR / "assets" / "lote_fundo" / "saida"

BRIGHTNESS = 1.05
CONTRAST = 1.10
COLOR = 1.00
DESKTOP_MAX_WIDTH = 1600
MOBILE_MAX_WIDTH = 900
OUTPUT_FORMAT = "WEBP"

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}


def _enhance(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(BRIGHTNESS)
    img = ImageEnhance.Contrast(img).enhance(CONTRAST)
    img = ImageEnhance.Color(img).enhance(COLOR)
    return img


def _remove_bg_and_white(img: Image.Image) -> Image.Image:
    rgba = remove(img)
    if rgba.mode != "RGBA":
        rgba = rgba.convert("RGBA")
    white_bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, rgba)
    return composited.convert("RGB")


def _resize(img: Image.Image, max_width: int) -> Image.Image:
    width, height = img.size
    if width <= max_width:
        return img
    new_height = int((max_width / width) * height)
    return img.resize((max_width, new_height), Image.LANCZOS)


def _process_file(src_path: Path, dst_base: Path) -> None:
    with Image.open(src_path) as img:
        cleaned = _remove_bg_and_white(img)
        cleaned = _enhance(cleaned)
        dst_base.parent.mkdir(parents=True, exist_ok=True)

        desktop = _resize(cleaned, DESKTOP_MAX_WIDTH)
        mobile = _resize(cleaned, MOBILE_MAX_WIDTH)

        desktop_path = dst_base.with_name(f"{dst_base.name}-desktop.webp")
        mobile_path = dst_base.with_name(f"{dst_base.name}-mobile.webp")

        desktop.save(desktop_path, OUTPUT_FORMAT, quality=82, method=6)
        mobile.save(mobile_path, OUTPUT_FORMAT, quality=82, method=6)


def _output_paths(dst_base: Path) -> tuple[Path, Path]:
    desktop_path = dst_base.with_name(f"{dst_base.name}-desktop.webp")
    mobile_path = dst_base.with_name(f"{dst_base.name}-mobile.webp")
    return desktop_path, mobile_path


def _already_processed(dst_base: Path) -> bool:
    desktop_path, mobile_path = _output_paths(dst_base)
    return desktop_path.exists() and mobile_path.exists()


def process_pending() -> int:
    if not ENTRADA_DIR.exists():
        raise FileNotFoundError(f"Pasta de entrada nao encontrada: {ENTRADA_DIR}")
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    for item in ENTRADA_DIR.iterdir():
        if not item.is_file():
            continue
        if item.suffix.lower() not in IMAGE_EXTS:
            continue
        dst_base = SAIDA_DIR / item.stem
        if _already_processed(dst_base):
            continue
        _process_file(item, dst_base)
        processed += 1
        print(f"Processado: {item.name} -> {dst_base.name}-desktop/mobile.webp")

    return processed


def main() -> None:
    processed = process_pending()
    print(f"Total processado: {processed}")


if __name__ == "__main__":
    main()
