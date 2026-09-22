import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def find_practice_root(start: Path) -> Path:
    current = start
    while current != current.parent:
        if (current / "Учебная практика 14.09.2026").is_dir():
            return current
        current = current.parent
    raise FileNotFoundError("не найден корень учебной практики")


ROOT = find_practice_root(HERE)
PRACTICE_14 = ROOT / "Учебная практика 14.09.2026"
BACKEND_DIR = PRACTICE_14 / "Интеграция с БД и агрегация данных (SQL + Backend)"
UI_DIR = PRACTICE_14 / "Разработка интерфейса (UI) по руководству по стилю"
FILL_DIR = PRACTICE_14 / "Наполнение интерфейса, отладка и стресс-тестирование"
sys.path.insert(0, str(FILL_DIR))
sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(HERE))

from catalog import load_cards, partner_to_card
from db import get_connection, initialize_database
from partner_service import get_partner_with_discount

UI_STATIC = UI_DIR / "static"
UI_RESOURCES = UI_DIR / "resources"


def open_db():
    connection = get_connection()
    initialize_database(connection)
    return connection


def load_partner_card(partner_id, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        partner = get_partner_with_discount(connection, partner_id)
        if partner is None:
            return None
        return partner_to_card(partner)
    finally:
        if own:
            connection.close()
