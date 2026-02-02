import os
import re
import unicodedata

import pandas as pd


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TABELA_PATH = os.path.join(BASE_DIR, "tabela_produtos_site.xlsx")
FOTOS_DIR = os.path.join(BASE_DIR, "assets", "fotos")


def _sanitize_folder_name(text: str) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return "Sem categoria"
    text = str(text).strip()
    if not text:
        return "Sem categoria"
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'[<>:"/\\|?*]', "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:120] if len(text) > 120 else text


def _sanitize_product_folder(code: str, title: str) -> str:
    code = "" if code is None or (isinstance(code, float) and pd.isna(code)) else str(code).strip()
    title = "" if title is None or (isinstance(title, float) and pd.isna(title)) else str(title).strip()
    name = f"{code} - {title}".strip(" -")
    name = unicodedata.normalize("NFKC", name)
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:140] if len(name) > 140 else name


def _write_info_file(folder: str, code: str, title: str, category: str) -> None:
    info_path = os.path.join(folder, ".produto.txt")
    if os.path.exists(info_path):
        return
    with open(info_path, "w", encoding="utf-8") as handle:
        handle.write(f"codigo={code}\n")
        handle.write(f"titulo={title}\n")
        handle.write(f"categoria={category}\n")


def main() -> None:
    if not os.path.exists(TABELA_PATH):
        raise FileNotFoundError(f"Tabela nao encontrada: {TABELA_PATH}")

    df = pd.read_excel(TABELA_PATH)
    required_cols = ["categoria", "codigo", "nome do produto no site"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatoria ausente: {col}")

    os.makedirs(FOTOS_DIR, exist_ok=True)
    created = 0

    for _, row in df.iterrows():
        category = _sanitize_folder_name(row.get("categoria"))
        code = row.get("codigo")
        title = row.get("nome do produto no site")
        product_folder = _sanitize_product_folder(code, title)
        if not product_folder:
            product_folder = _sanitize_product_folder(code or "SEM-CODIGO", title or "Sem titulo")

        category_dir = os.path.join(FOTOS_DIR, category)
        product_dir = os.path.join(category_dir, product_folder)
        os.makedirs(product_dir, exist_ok=True)
        _write_info_file(product_dir, str(code or ""), str(title or ""), category)
        created += 1

    print(f"Pastas criadas/confirmadas: {created}")


if __name__ == "__main__":
    main()
