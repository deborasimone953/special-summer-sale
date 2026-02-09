"""Servidor local para seleção de capas dos produtos."""
import http.server
import json
import os
import re

PORT = 8888
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

class CoverHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PROJECT_DIR, **kwargs)

    def do_POST(self):
        if self.path == '/save-covers':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            new_order = json.loads(body)

            # Read current index.html
            index_path = os.path.join(PROJECT_DIR, 'index.html')
            with open(index_path, 'r', encoding='utf-8') as f:
                html = f.read()

            # Find productImagesByCode block
            pattern = r'(const\s+productImagesByCode\s*=\s*)\{([\s\S]*?)\};'
            match = re.search(pattern, html)
            if not match:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'productImagesByCode not found')
                return

            # Parse current object
            full_match = match.group(0)
            obj_str = '{' + match.group(2) + '}'
            try:
                current = json.loads(obj_str)
            except json.JSONDecodeError:
                # Fallback: use regex to avoid eval
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b'Failed to parse productImagesByCode JSON')
                return

            # Update with new order (only the codes that were reordered)
            for code, images in new_order.items():
                current[code] = images

            # Rebuild JSON block
            new_json = json.dumps(current, indent=2, ensure_ascii=False)
            new_block = match.group(1) + new_json + ';'
            html = html[:match.start()] + new_block + html[match.end():]

            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)

            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Capas atualizadas para {len(new_order)} produtos.'.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    print(f'Servidor rodando em http://localhost:{PORT}')
    print(f'Abra http://localhost:{PORT}/cover-selector.html no navegador')
    server = http.server.HTTPServer(('', PORT), CoverHandler)
    server.serve_forever()
