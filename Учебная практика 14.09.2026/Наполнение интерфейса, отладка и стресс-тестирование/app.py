from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import webbrowser

from catalog import UI_RESOURCES, UI_STATIC, load_cards
from page import render_page

PORT = 8766

MIME = {
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


class CRMHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path == "/" or path == "/index.html":
            body = render_page(load_cards()).encode("utf-8")
            self._send(200, "text/html; charset=utf-8", body)
            return
        if path.startswith("/static/"):
            self._send_file(UI_STATIC / path.removeprefix("/static/"))
            return
        if path.startswith("/resources/"):
            self._send_file(UI_RESOURCES / path.removeprefix("/resources/"))
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def _send(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, file_path: Path):
        file_path = file_path.resolve()
        allowed = (UI_STATIC.resolve(), UI_RESOURCES.resolve())
        if not any(file_path.is_relative_to(root) for root in allowed) or not file_path.is_file():
            self._send(404, "text/plain; charset=utf-8", b"Not found")
            return
        content_type = MIME.get(file_path.suffix.lower(), "application/octet-stream")
        self._send(200, content_type, file_path.read_bytes())


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), CRMHandler)
    url = f"http://127.0.0.1:{PORT}/"
    print(url)
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
        server.server_close()


if __name__ == "__main__":
    main()
