import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRACTICE_DIR = HERE.parent
BACKEND_DIR = PRACTICE_DIR / "Интеграция с БД и агрегация данных (SQL + Backend)"
UI_DIR = PRACTICE_DIR / "Разработка интерфейса (UI) по руководству по стилю"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(UI_DIR))
sys.path.insert(0, str(HERE))

from db import get_connection, initialize_database
from partner_service import list_partners_with_discount, quantity_or_zero
from partner_discount import calculate_partner_discount
from partners import DIRECTORS, format_rating, split_type_and_name

UI_STATIC = UI_DIR / "static"
UI_RESOURCES = UI_DIR / "resources"

RAW_SUM_SQL = """
SELECT SUM(sales_history.quantity) AS total_quantity
FROM partners
LEFT JOIN sales_history
    ON sales_history.partner_id = partners.partner_id
WHERE partners.partner_id = ?
"""


def discount_or_zero(discount, total_quantity=0) -> int:
    if discount is None:
        return calculate_partner_discount(quantity_or_zero(total_quantity))
    try:
        return int(discount)
    except (TypeError, ValueError):
        return calculate_partner_discount(quantity_or_zero(total_quantity))


def raw_sales_sum(connection, partner_id):
    row = connection.execute(RAW_SUM_SQL, (partner_id,)).fetchone()
    if row is None:
        return None
    return row["total_quantity"]


def partner_to_card(partner: dict) -> dict:
    partner_type, short_name = split_type_and_name(partner["company_name"])
    total_quantity = quantity_or_zero(partner.get("total_quantity"))
    return {
        "partner_id": partner["partner_id"],
        "partner_type": partner_type,
        "company_name": short_name,
        "director": DIRECTORS.get(partner["partner_id"], "—"),
        "contact_email": partner.get("contact_email") or "—",
        "phone": partner.get("phone") or "—",
        "rating": format_rating(partner.get("rating")),
        "total_quantity": total_quantity,
        "discount_percent": discount_or_zero(
            partner.get("discount_percent"), total_quantity
        ),
    }


def load_cards(connection=None):
    own_connection = connection is None
    if own_connection:
        connection = get_connection()
        initialize_database(connection)
    try:
        partners = list_partners_with_discount(connection)
        return [partner_to_card(partner) for partner in partners]
    finally:
        if own_connection:
            connection.close()
