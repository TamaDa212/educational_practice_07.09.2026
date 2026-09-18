import sys
from pathlib import Path

DISCOUNT_DIR = Path(__file__).resolve().parent.parent / "Разработка ядра бизнес-логики (Расчет скидки)"
sys.path.insert(0, str(DISCOUNT_DIR))

from partner_discount import calculate_partner_discount

PARTNER_SALES_SQL = """
SELECT
    partners.partner_id,
    partners.company_name,
    partners.inn,
    partners.contact_email,
    partners.phone,
    partners.rating,
    COALESCE(SUM(sales_history.quantity), 0) AS total_quantity
FROM partners
LEFT JOIN sales_history
    ON sales_history.partner_id = partners.partner_id
WHERE partners.partner_id = ?
GROUP BY
    partners.partner_id,
    partners.company_name,
    partners.inn,
    partners.contact_email,
    partners.phone,
    partners.rating
"""


def quantity_or_zero(value) -> int:
    if value is None:
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def get_partner_sales_total(connection, partner_id):
    cursor = connection.cursor()
    cursor.execute(PARTNER_SALES_SQL, (partner_id,))
    row = cursor.fetchone()
    return row


def get_partner_with_discount(connection, partner_id):
    row = get_partner_sales_total(connection, partner_id)
    if row is None:
        return None
    total_quantity = quantity_or_zero(row["total_quantity"])
    discount_percent = calculate_partner_discount(total_quantity)
    partner_data = {
        "partner_id": row["partner_id"],
        "company_name": row["company_name"],
        "inn": row["inn"],
        "contact_email": row["contact_email"],
        "phone": row["phone"],
        "rating": row["rating"],
        "total_quantity": total_quantity,
        "discount_percent": discount_percent,
    }
    return partner_data


def list_partners_with_discount(connection):
    cursor = connection.execute(
        "SELECT partner_id FROM partners ORDER BY partner_id"
    )
    partners = []
    for row in cursor.fetchall():
        partner = get_partner_with_discount(connection, row["partner_id"])
        if partner is not None:
            partners.append(partner)
    return partners
