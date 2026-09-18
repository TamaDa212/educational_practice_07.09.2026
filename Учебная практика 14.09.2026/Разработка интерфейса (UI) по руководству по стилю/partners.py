import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRACTICE_DIR = HERE.parent
BACKEND_DIR = PRACTICE_DIR / "Интеграция с БД и агрегация данных (SQL + Backend)"
DISCOUNT_DIR = PRACTICE_DIR / "Разработка ядра бизнес-логики (Расчет скидки)"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(DISCOUNT_DIR))

from db import get_connection, initialize_database
from partner_discount import calculate_partner_discount

TYPE_PREFIXES = ("ООО", "ИП", "ТК", "ТД", "ПАО", "ЗАО", "ОАО", "АО")

DIRECTORS = {
    1: "Иванов И.И.",
    2: "Петров А.В.",
    3: "Сидоров С.П.",
    4: "Кузнецова А.Н.",
    5: "Смирнов Д.В.",
}

PARTNERS_SQL = """
SELECT
    partners.partner_id,
    partners.company_name,
    partners.phone,
    partners.rating,
    COALESCE(SUM(sales_history.quantity), 0) AS total_quantity
FROM partners
LEFT JOIN sales_history
    ON sales_history.partner_id = partners.partner_id
GROUP BY
    partners.partner_id,
    partners.company_name,
    partners.phone,
    partners.rating
ORDER BY partners.partner_id
"""


def split_type_and_name(company_name: str) -> tuple[str, str]:
    name = company_name.strip()
    for prefix in TYPE_PREFIXES:
        if name.startswith(prefix):
            rest = name[len(prefix) :].strip().strip('"«»')
            return prefix, rest or name
    return "Партнёр", name


def format_rating(rating) -> str:
    if rating is None:
        return "—"
    value = float(rating)
    if value.is_integer():
        return str(int(value))
    return str(value)


def list_partners(connection=None):
    own_connection = connection is None
    if own_connection:
        connection = get_connection()
        initialize_database(connection)
    try:
        rows = connection.execute(PARTNERS_SQL).fetchall()
        partners = []
        for row in rows:
            partner_type, short_name = split_type_and_name(row["company_name"])
            total_quantity = int(row["total_quantity"])
            partners.append(
                {
                    "partner_id": row["partner_id"],
                    "partner_type": partner_type,
                    "company_name": short_name,
                    "director": DIRECTORS.get(row["partner_id"], "—"),
                    "phone": row["phone"] or "—",
                    "rating": format_rating(row["rating"]),
                    "discount_percent": calculate_partner_discount(total_quantity),
                }
            )
        return partners
    finally:
        if own_connection:
            connection.close()
