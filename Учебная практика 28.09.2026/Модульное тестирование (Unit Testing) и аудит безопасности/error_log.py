from datetime import datetime
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent / "app.log"


def log_error(message, log_path=None):
    moment = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    path = LOG_PATH if log_path is None else log_path
    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(f"{moment} | {message}\n")


def guard(action, log_path=None):
    try:
        return action()
    except Exception as error:
        log_error(f"Ошибка: {error}", log_path)
        return -1
