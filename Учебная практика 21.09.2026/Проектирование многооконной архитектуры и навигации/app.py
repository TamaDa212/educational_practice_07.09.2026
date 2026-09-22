from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import webbrowser

from data import UI_RESOURCES, UI_STATIC, load_partner_card, load_sales
from catalog import load_cards
from navigation import HISTORY, LIST, MISSING, PARTNER, Navigator
from screens import render_screen

HERE = Path(__file__).resolve().parent
LOCAL_STATIC = HERE / "static"
PORT = 8767
NAVIGATOR = Navigator()

MIME = {
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
}


def page_for(screen, params):
    trail = NAVIGATOR.trail()
    selected = NAVIGATOR.selected_partner_id
    if screen == LIST:
        return render_screen(
            LIST, params, partners=load_cards(), selected_partner_id=selected, trail=trail
        )
    if screen in {PARTNER, HISTORY}:
        partner_id = params.get("partner_id")
        partner = load_partner_card(partner_id)
        if partner is None:
            params = {"partner_id": partner_id}
            NAVIGATOR.stack = [(LIST, {}), (MISSING, params)]
            return render_screen(MISSING, params, trail=NAVIGATOR.trail())
        sales = load_sales(partner_id) if screen == HISTORY else None
        return render_screen(
            screen,
            params,
            partner=partner,
            sales=sales,
            selected_partner_id=selected,
            trail=trail,
        )
    return render_screen(MISSING, params, trail=trail)


class CRMHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path.startswith("/static/"):
            self._send_file(self._static_file(path.removeprefix("/static/")))
            return
        if path.startswith("/resources/"):
            self._send_file(UI_RESOURCES / path.removeprefix("/resources/"))
            return
        if path == "/back":
            screen, params = NAVIGATOR.back()
            html = page_for(screen, params)
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        if path in {"/", "/index.html", "/partners"}:
            screen, params = NAVIGATOR.open_list()
            html = page_for(screen, params)
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        parts = [item for item in path.split("/") if item]
        if len(parts) >= 2 and parts[0] == "partner":
            partner_id = parts[1]
            if len(parts) >= 3 and parts[2] == "history":
                screen, params = NAVIGATOR.open_history(partner_id)
            else:
                screen, params = NAVIGATOR.open_partner(partner_id)
            html = page_for(screen, params)
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

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
