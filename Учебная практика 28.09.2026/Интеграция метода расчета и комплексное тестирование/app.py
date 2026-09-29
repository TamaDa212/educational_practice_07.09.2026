from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import webbrowser

from form_page import render_calculator
from order_calculator import calculate_order

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
PORT = 8772

MIME = {
    ".css": "text/css; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
}

EMPTY_VALUES = {
    "product_type_id": "",
    "material_type_id": "",
    "quantity": "",
    "param_1": "",
    "param_2": "",
}


def values_from_post(fields):
    values = {}
    for name in EMPTY_VALUES:
        raw = fields.get(name, [""])
        if raw:
            values[name] = raw[0].strip()
        else:
            values[name] = ""
    return values


class CalculatorHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path.startswith("/static/"):
            self._send_file(self._static_file(path.removeprefix("/static/")))
            return
        if path.startswith("/resources/"):
            self._send_file(UI_RESOURCES / path.removeprefix("/resources/"))
            return
        if path in {"/", "/index.html"}:
            html = render_calculator(EMPTY_VALUES)
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        if path != "/calculate":
            self._send(404, "text/plain; charset=utf-8", b"Not found")
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length).decode("utf-8")
        fields = parse_qs(raw, keep_blank_values=True)
        values = values_from_post(fields)
        result = calculate_order(
            values["product_type_id"],
            values["material_type_id"],
            values["quantity"],
            values["param_1"],
            values["param_2"],
        )
        html = render_calculator(values, result)
        self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))

    def _static_file(self, name):
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

    def _send_file(self, file_path):
        file_path = file_path.resolve()
        allowed = (LOCAL_STATIC.resolve(), UI_STATIC.resolve(), UI_RESOURCES.resolve())
        inside = False
        for root in allowed:
            if file_path.is_relative_to(root):
                inside = True
        if not inside or not file_path.is_file():
            self._send(404, "text/plain; charset=utf-8", b"Not found")
            return
        content_type = MIME.get(file_path.suffix.lower(), "application/octet-stream")
        self._send(200, content_type, file_path.read_bytes())


def main():
    server = ThreadingHTTPServer(("127.0.0.1", PORT), CalculatorHandler)
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
