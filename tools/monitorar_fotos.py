import os
import re
import time
import unicodedata
from shutil import copyfile

from PIL import Image


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOTOS_DIR = os.path.join(BASE_DIR, "assets", "fotos")
SLEEP_SECONDS = 2
DESKTOP_MAX_WIDTH = 1600
MOBILE_MAX_WIDTH = 900
DERIVATIVE_FORMAT = "webp"
COVER_FILE_NAME = ".capa.txt"

COVER_MARKER_RE = re.compile(r"(^|[\s_\-\(\[])(capa)([\s_\-\)\]]|$)", re.IGNORECASE)


def _sanitize_title(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'[<>:"/\\|?*]', "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:120] if len(text) > 120 else text


def _read_title(folder: str) -> str:
    info_path = os.path.join(folder, ".produto.txt")
    if not os.path.exists(info_path):
        return os.path.basename(folder)
    title = None
    with open(info_path, "r", encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("titulo="):
                title = line.split("=", 1)[1].strip()
                break
    return title or os.path.basename(folder)


def _next_index(folder: str, title: str) -> int:
    prefix = f"{title}-"
    max_idx = 0
    for entry in os.scandir(folder):
        if not entry.is_file():
            continue
        name, _ext = os.path.splitext(entry.name)
        if _is_derivative_name(name):
            continue
        if not name.startswith(prefix):
            continue
        suffix = name[len(prefix) :]
        if suffix.isdigit():
            max_idx = max(max_idx, int(suffix))
    return max_idx + 1


def _should_rename(file_name: str) -> bool:
    if file_name.startswith("."):
        return False
    return True


def _is_derivative_name(name: str) -> bool:
    return name.endswith("-desktop") or name.endswith("-mobile")


def _is_image_ext(ext: str) -> bool:
    return ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"]


def _has_cover_marker(name: str) -> bool:
    return bool(COVER_MARKER_RE.search(name))


def _strip_cover_marker(name: str) -> str:
    cleaned = COVER_MARKER_RE.sub(" ", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _resize_and_save(src_path: str, dest_path: str, max_width: int) -> None:
    with Image.open(src_path) as img:
        img_format = img.format or DERIVATIVE_FORMAT
        if img_format.upper() == "GIF":
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


def _ensure_derivatives(image_path: str) -> None:
    base, _ext = os.path.splitext(image_path)
    desktop_path = f"{base}-desktop.{DERIVATIVE_FORMAT}"
    mobile_path = f"{base}-mobile.{DERIVATIVE_FORMAT}"

    if not os.path.exists(desktop_path):
        _resize_and_save(image_path, desktop_path, DESKTOP_MAX_WIDTH)
        print(f"Gerado: {desktop_path}")
    if not os.path.exists(mobile_path):
        _resize_and_save(image_path, mobile_path, MOBILE_MAX_WIDTH)
        print(f"Gerado: {mobile_path}")


def _set_cover_image(image_path: str) -> None:
    folder = os.path.dirname(image_path)
    base, _ext = os.path.splitext(os.path.basename(image_path))
    cover_info_path = os.path.join(folder, COVER_FILE_NAME)
    with open(cover_info_path, "w", encoding="utf-8") as handle:
        handle.write(f"{base}\n")

    desktop_src = os.path.join(folder, f"{base}-desktop.{DERIVATIVE_FORMAT}")
    mobile_src = os.path.join(folder, f"{base}-mobile.{DERIVATIVE_FORMAT}")
    desktop_cover = os.path.join(folder, f"capa-desktop.{DERIVATIVE_FORMAT}")
    mobile_cover = os.path.join(folder, f"capa-mobile.{DERIVATIVE_FORMAT}")

    if os.path.exists(desktop_src):
        copyfile(desktop_src, desktop_cover)
    if os.path.exists(mobile_src):
        copyfile(mobile_src, mobile_cover)
    print(f"Capa definida: {base}")


def _rename_new_files_in_folder(folder: str) -> None:
    title = _sanitize_title(_read_title(folder))
    if not title:
        title = "produto"

    for entry in os.scandir(folder):
        if not entry.is_file():
            continue
        if not _should_rename(entry.name):
            continue

        name, ext = os.path.splitext(entry.name)
        ext_lower = ext.lower()
        if _is_derivative_name(name):
            continue
        if not _is_image_ext(ext_lower):
            continue
        is_cover = _has_cover_marker(name)

        clean_name = _strip_cover_marker(name) if is_cover else name
        if clean_name.startswith(f"{title}-") and clean_name[len(title) + 1 :].isdigit():
            if clean_name != name:
                new_name = f"{clean_name}{ext_lower}"
                new_path = os.path.join(folder, new_name)
                os.rename(entry.path, new_path)
                entry_path = new_path
            else:
                entry_path = entry.path
            _ensure_derivatives(entry_path)
            if is_cover:
                _set_cover_image(entry_path)
            continue

        next_idx = _next_index(folder, title)
        new_name = f"{title}-{next_idx:02d}{ext_lower}"
        new_path = os.path.join(folder, new_name)
        os.rename(entry.path, new_path)
        print(f"Renomeado: {entry.path} -> {new_path}")
        _ensure_derivatives(new_path)
        if is_cover:
            _set_cover_image(new_path)


def main() -> None:
    if not os.path.exists(FOTOS_DIR):
        raise FileNotFoundError(f"Pasta de fotos nao encontrada: {FOTOS_DIR}")

    print(f"Monitorando {FOTOS_DIR}... (Ctrl+C para sair)")
    while True:
        for root, dirs, _files in os.walk(FOTOS_DIR):
            for d in dirs:
                folder = os.path.join(root, d)
                _rename_new_files_in_folder(folder)
        time.sleep(SLEEP_SECONDS)


if __name__ == "__main__":
    main()
