import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PRACTICE_14 = ROOT / "Учебная практика 14.09.2026"
BACKEND_DIR = PRACTICE_14 / "Интеграция с БД и агрегация данных (SQL + Backend)"
UI_DIR = PRACTICE_14 / "Разработка интерфейса (UI) по руководству по стилю"
FILL_DIR = PRACTICE_14 / "Наполнение интерфейса, отладка и стресс-тестирование"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(FILL_DIR))

from catalog import load_cards, partner_to_card
from db import get_connection, initialize_database
from partner_service import get_partner_with_discount

UI_STATIC = UI_DIR / "static"
UI_RESOURCES = UI_DIR / "resources"

SALES_SQL = """
SELECT
    sales_history.sale_id,
    sales_history.sale_date,
    products.product_name,
    sales_history.quantity,
    sales_history.total_amount
FROM sales_history
INNER JOIN products
    ON products.product_id = sales_history.product_id
WHERE sales_history.partner_id = ?
ORDER BY sales_history.sale_date
"""


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


def load_sales(partner_id, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        rows = connection.execute(SALES_SQL, (partner_id,)).fetchall()
        sales = []
        for row in rows:
            sales.append(
                {
                    "sale_id": row["sale_id"],
                    "sale_date": row["sale_date"],
                    "product_name": row["product_name"],
                    "quantity": int(row["quantity"] or 0),
                    "total_amount": float(row["total_amount"] or 0),
                }
            )
        return sales
    finally:
        if own:
            connection.close()
