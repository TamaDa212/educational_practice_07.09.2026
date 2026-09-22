import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse
import webbrowser

from db import open_db
from messagebox import MessageBox
from navigation import EDIT, LIST, MISSING, Navigator, parse_partner_id
from partner_crud import IntegrityError, get_partner, list_partners, save_partner
from partner_edit import PartnerEditWindow, values_from_partner, values_from_post
from screens import render_screen
from validation import ValidationError, validate_partner

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
PORT = 8770
NAVIGATOR = Navigator()

MIME = {
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".png": "image/png",
    ".ico": "image/x-icon",
}

DB_ERROR = (
    "СУБД недоступна. Проверьте, что файл базы данных не заблокирован, "
    "и повторите сохранение."
)
SAVE_OK_ADD = "Партнёр успешно добавлен в базу данных."
SAVE_OK_EDIT = "Изменения партнёра успешно сохранены в базу данных."


def edit_window(partner_id, values=None, dialog=None):
    parsed = parse_partner_id(partner_id)
    if values is None:
        if parsed is None:
            values = None
        else:
            partner = get_partner(parsed)
            if partner is None:
                return None
            values = values_from_partner(partner)
    return PartnerEditWindow(partner_id=parsed, values=values, dialog=dialog)


def page_for(screen, params, window=None):
    trail = NAVIGATOR.trail()
    selected = NAVIGATOR.selected_partner_id
    if screen == LIST:
        return render_screen(
            LIST,
            params,
            partners=list_partners(),
            selected_partner_id=selected,
            trail=trail,
            dialog=NAVIGATOR.dialog,
        )
    if screen == EDIT:
        if window is None:
            window = edit_window(params.get("partner_id"))
        if window is None:
            params = {"partner_id": params.get("partner_id")}
            NAVIGATOR.stack = [(LIST, {}), (MISSING, params)]
            return render_screen(
                MISSING,
                params,
                trail=NAVIGATOR.trail(),
                dialog=MessageBox.error(
                    "Партнер не найден. Вернитесь к списку и выберите существующую запись."
                ),
            )
        return render_screen(EDIT, params, window=window, trail=trail)
    return render_screen(MISSING, params, trail=trail, dialog=NAVIGATOR.dialog)


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
            html = page_for(*NAVIGATOR.back())
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        if path in {"/", "/index.html", "/partners"}:
            html = page_for(*NAVIGATOR.open_list(NAVIGATOR.dialog))
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        if path in {"/partner/new", "/partner/edit"}:
            html = page_for(*NAVIGATOR.open_edit(None))
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        parts = [item for item in path.split("/") if item]
        if len(parts) >= 2 and parts[0] == "partner":
            html = page_for(*NAVIGATOR.open_edit(parts[1]))
            self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))
            return
        self._send(404, "text/plain; charset=utf-8", b"Not found")

    def do_POST(self):
        path = unquote(urlparse(self.path).path)
        if path != "/partner/save":
            self._send(404, "text/plain; charset=utf-8", b"Not found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0") or 0)
            raw = self.rfile.read(length).decode("utf-8")
            fields = parse_qs(raw, keep_blank_values=True)
            partner_id = parse_partner_id((fields.get("partner_id") or [""])[0])
            values = values_from_post(fields)
            cleaned = validate_partner(values)
            saved = save_partner(partner_id, cleaned)
        except ValidationError as exc:
            self._show_error(partner_id if "partner_id" in locals() else None, values if "values" in locals() else None, exc.message)
            return
        except IntegrityError as exc:
            self._show_error(partner_id, values, str(exc) + " Исправьте данные и повторите попытку.")
            return
        except sqlite3.Error:
            self._show_error(partner_id if "partner_id" in locals() else None, values if "values" in locals() else None, DB_ERROR)
            return
        except Exception:
            self._show_error(
                None,
                None,
                "Операция прервана из‑за ошибки ввода. Проверьте поля формы и повторите попытку.",
            )
            return
        text = SAVE_OK_ADD if partner_id is None else SAVE_OK_EDIT
        NAVIGATOR.selected_partner_id = saved["partner_id"]
        NAVIGATOR.open_list(MessageBox.information(text))
        self._redirect("/")

    def _show_error(self, partner_id, values, text):
        NAVIGATOR.open_edit(partner_id)
        window = PartnerEditWindow(
            partner_id, values, dialog=MessageBox.error(text)
        )
        html = page_for(EDIT, NAVIGATOR.params, window=window)
        self._send(200, "text/html; charset=utf-8", html.encode("utf-8"))

    def _redirect(self, location):
        self.send_response(303)
        self.send_header("Location", location)
        self.send_header("Content-Length", "0")
        self.end_headers()

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
