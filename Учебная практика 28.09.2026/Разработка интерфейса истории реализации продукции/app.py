from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import webbrowser

from db import open_db
from history_window import PartnerHistoryWindow
from sales_history import get_partner, list_partners, load_shipments
from screens import render_history, render_list, render_missing

HERE = Path(__file__).resolve().parent
current = HERE
while current != current.parent:
    ui = current / "Учебная практика 14.09.2026" / "Разработка интерфейса (UI) по руководству по стилю"
    if ui.is_dir():
        UI_DIR = ui
        break
    current = current.parent
else:
    raise FileNotFoundError("не найден каталог UI")

UI_STATIC = UI_DIR / "static"
UI_RESOURCES = UI_DIR / "resources"
LOCAL_STATIC = HERE / "static"
PORT = 8771

# Выбранный на главной форме партнёр: его id уходит в PartnerHistoryWindow.
SELECTED_PARTNER_ID = None

MIME = {
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
}


def parse_partner_id(value):
    try:
        partner_id = int(value)
    except (TypeError, ValueError):
        return None
    if partner_id <= 0:
        return None
    return partner_id


class CRMHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        global SELECTED_PARTNER_ID
        path = unquote(urlparse(self.path).path)
        if path.startswith("/static/"):
            self._send_file(self._static_file(path.removeprefix("/static/")))
            return
        if path.startswith("/resources/"):
            self._send_file(UI_RESOURCES / path.removeprefix("/resources/"))
            return
        if path in {"/", "/index.html", "/partners"}:
            html = render_list(list_partners(), SELECTED_PARTNER_ID)
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        if path == "/history":
            self._open_history(SELECTED_PARTNER_ID)
            return
        parts = [item for item in path.split("/") if item]
        if len(parts) >= 2 and parts[0] == "partner":
            partner_id = parse_partner_id(parts[1])
            if len(parts) >= 3 and parts[2] == "history":
                self._open_history(partner_id)
                return
            if partner_id is None:
                html = render_missing(parts[1])
            else:
                SELECTED_PARTNER_ID = partner_id
                html = render_list(list_partners(), SELECTED_PARTNER_ID)
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def _open_history(self, partner_id):
        global SELECTED_PARTNER_ID
        if partner_id is None:
            html = render_list(
                list_partners(),
                None,
                notice="Сначала выберите партнера в списке, затем нажмите «История продаж».",
            )
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        partner = get_partner(partner_id)
        if partner is None:
            html = render_missing(partner_id)
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        SELECTED_PARTNER_ID = partner_id
        window = PartnerHistoryWindow(partner, load_shipments(partner_id))
        html = render_history(window)
        self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))

    def _static_file(self, name: str) -> Path:
        local = (LOCAL_STATIC / name).resolve()
        if local.is_file() and local.is_relative_to(LOCAL_STATIC.resolve()):
            return local
        return UI_STATIC / name

    def _send(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, file_path: Path):
        file_path = file_path.resolve()
        allowed = (LOCAL_STATIC.resolve(), UI_STATIC.resolve(), UI_RESOURCES.resolve())
        if not any(file_path.is_relative_to(root) for root in allowed) or not file_path.is_file():
            self._send(404, "text/plain; charset=utf-8", b"Not found")
            return
        content_type = MIME.get(file_path.suffix.lower(), "application/octet-stream")
        self._send(200, content_type, file_path.read_bytes())


def main():
    open_db()
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
