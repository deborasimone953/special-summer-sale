import json
import os
import re
import unicodedata
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOTOS_DIR = os.path.join(BASE_DIR, "assets", "fotos")
HOST = "127.0.0.1"
PORT = 8000
DESKTOP_MAX_WIDTH = 1600
MOBILE_MAX_WIDTH = 900
DERIVATIVE_FORMAT = "webp"
COVER_FILE_NAME = ".capa.txt"

IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"]


def _is_derivative_name(name: str) -> bool:
    return name.endswith("-desktop") or name.endswith("-mobile")


def _safe_join(base: str, *paths: str) -> str:
    joined = os.path.abspath(os.path.join(base, *paths))
    if not joined.startswith(base):
        raise ValueError("Caminho invalido")
    return joined


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


def _sanitize_title(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r'[<>:"/\\|?*]', "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:120] if len(text) > 120 else text


def _resize_and_save(src_path: str, dest_path: str, max_width: int) -> None:
    if Image is None:
        raise RuntimeError("Pillow não está instalado. Instale com: pip install pillow")
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
    if not os.path.exists(mobile_path):
        _resize_and_save(image_path, mobile_path, MOBILE_MAX_WIDTH)


def _set_cover_image(image_path: str) -> str:
    folder = os.path.dirname(image_path)
    base, _ext = os.path.splitext(os.path.basename(image_path))

    if Image is not None:
        _ensure_derivatives(image_path)
    cover_info_path = os.path.join(folder, COVER_FILE_NAME)
    with open(cover_info_path, "w", encoding="utf-8") as handle:
        handle.write(f"{base}\n")
    return base


def _list_products() -> list[dict]:
    products = []
    for category in sorted(os.listdir(FOTOS_DIR)):
        category_path = os.path.join(FOTOS_DIR, category)
        if not os.path.isdir(category_path):
            continue
        for product in sorted(os.listdir(category_path)):
            product_path = os.path.join(category_path, product)
            if not os.path.isdir(product_path):
                continue
            title = _sanitize_title(_read_title(product_path))
            images = []
            for entry in os.scandir(product_path):
                if not entry.is_file():
                    continue
                if entry.name.startswith("."):
                    continue
                name, ext = os.path.splitext(entry.name)
                if _is_derivative_name(name):
                    continue
                if ext.lower() not in IMAGE_EXTS:
                    continue
                rel_path = os.path.relpath(entry.path, FOTOS_DIR).replace("\\", "/")
                images.append(rel_path)
            if images:
                products.append(
                    {
                        "categoria": category,
                        "produto": product,
                        "titulo": title or product,
                        "pasta": os.path.relpath(product_path, FOTOS_DIR).replace("\\", "/"),
                        "imagens": images,
                    }
                )
    return products


INDEX_HTML = """<!doctype html>
<html lang="pt-br">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Selecionar capa</title>
    <style>
      body { font-family: Arial, sans-serif; margin: 0; background: #f6f6f6; }
      header { padding: 12px 16px; background: #222; color: #fff; }
      main { display: grid; grid-template-columns: 320px 1fr; gap: 16px; padding: 16px; }
      .list { background: #fff; border-radius: 8px; padding: 8px; max-height: calc(100vh - 120px); overflow: auto; }
      .item { padding: 8px 10px; border-bottom: 1px solid #eee; cursor: pointer; }
      .item.active { background: #e9f4ff; }
      .gallery { background: #fff; border-radius: 8px; padding: 12px; min-height: 300px; }
      .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 10px; }
      .card { border: 2px solid transparent; border-radius: 6px; overflow: hidden; background: #fafafa; }
      .card.active { border-color: #1a73e8; }
      .card img { width: 100%; height: 160px; object-fit: cover; display: block; }
      .card button { width: 100%; border: none; padding: 8px; cursor: pointer; background: #1a73e8; color: white; }
      .empty { color: #666; padding: 16px; }
    </style>
  </head>
  <body>
    <header>Selecionar foto de capa</header>
    <main>
      <section class="list" id="productList"></section>
      <section class="gallery">
        <h3 id="productTitle">Selecione um produto</h3>
        <div id="imageGrid" class="grid"></div>
        <div id="emptyState" class="empty" style="display:none;">Nenhuma imagem encontrada</div>
      </section>
    </main>
    <script>
      const listEl = document.getElementById("productList");
      const gridEl = document.getElementById("imageGrid");
      const titleEl = document.getElementById("productTitle");
      const emptyEl = document.getElementById("emptyState");
      let products = [];
      let current = null;

      function renderList() {
        listEl.innerHTML = "";
        products.forEach((p, idx) => {
          const div = document.createElement("div");
          div.className = "item" + (current === idx ? " active" : "");
          div.textContent = `${p.titulo} (${p.categoria})`;
          div.onclick = () => selectProduct(idx);
          listEl.appendChild(div);
        });
      }

      function selectProduct(idx) {
        current = idx;
        renderList();
        const p = products[idx];
        titleEl.textContent = p.titulo;
        gridEl.innerHTML = "";
        if (!p.imagens.length) {
          emptyEl.style.display = "block";
          return;
        }
        emptyEl.style.display = "none";
        p.imagens.forEach((img) => {
          const card = document.createElement("div");
          card.className = "card";
          const image = document.createElement("img");
          image.src = `/fotos/${img}`;
          image.loading = "lazy";
          const btn = document.createElement("button");
          btn.textContent = "Definir como capa";
          btn.onclick = async () => {
            await fetch("/api/cover", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ pasta: p.pasta, imagem: img }),
            });
            alert("Capa definida!");
          };
          card.appendChild(image);
          card.appendChild(btn);
          gridEl.appendChild(card);
        });
      }

      async function loadProducts() {
        const res = await fetch("/api/products");
        products = await res.json();
        renderList();
        if (products.length) selectProduct(0);
      }

      loadProducts();
    </script>
  </body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/":
            self._send(200, INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return

        if self.path.startswith("/api/products"):
            data = json.dumps(_list_products(), ensure_ascii=False).encode("utf-8")
            self._send(200, data, "application/json; charset=utf-8")
            return

        if self.path.startswith("/fotos/"):
            rel = unquote(self.path[len("/fotos/") :])
            try:
                target = _safe_join(FOTOS_DIR, rel)
            except ValueError:
                self._send(400, b"Caminho invalido", "text/plain; charset=utf-8")
                return
            if not os.path.exists(target):
                self._send(404, b"Nao encontrado", "text/plain; charset=utf-8")
                return
            with open(target, "rb") as handle:
                data = handle.read()
            ext = os.path.splitext(target)[1].lower()
            ctype = "application/octet-stream"
            if ext in [".jpg", ".jpeg"]:
                ctype = "image/jpeg"
            elif ext == ".png":
                ctype = "image/png"
            elif ext == ".webp":
                ctype = "image/webp"
            elif ext == ".gif":
                ctype = "image/gif"
            self._send(200, data, ctype)
            return

        self._send(404, b"Nao encontrado", "text/plain; charset=utf-8")

    def do_POST(self) -> None:
        if self.path != "/api/cover":
            self._send(404, b"Nao encontrado", "text/plain; charset=utf-8")
            return
        content_length = int(self.headers.get("Content-Length", "0"))
        payload = self.rfile.read(content_length)
        try:
            data = json.loads(payload.decode("utf-8"))
            pasta = data.get("pasta")
            imagem = data.get("imagem")
        except Exception:
            self._send(400, b"JSON invalido", "text/plain; charset=utf-8")
            return

        try:
            image_path = _safe_join(FOTOS_DIR, imagem)
            if not os.path.exists(image_path):
                raise FileNotFoundError("Imagem nao encontrada")
            if pasta:
                folder_path = _safe_join(FOTOS_DIR, pasta)
                if not image_path.startswith(folder_path):
                    raise ValueError("Imagem fora da pasta informada")
        except Exception:
            self._send(400, b"Caminho invalido", "text/plain; charset=utf-8")
            return

        cover_base = _set_cover_image(image_path)
        resp = json.dumps({"ok": True, "capa": cover_base}, ensure_ascii=False).encode("utf-8")
        self._send(200, resp, "application/json; charset=utf-8")


def main() -> None:
    if not os.path.exists(FOTOS_DIR):
        raise FileNotFoundError(f"Pasta de fotos nao encontrada: {FOTOS_DIR}")
    print(f"Abrindo em http://{HOST}:{PORT}")
    server = HTTPServer((HOST, PORT), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
