from datetime import datetime

from db import open_db

# JOIN связывает отгрузку с названием продукции: в sales_history хранится только product_id.
HISTORY_SQL = """
SELECT
    products.product_name,
    sales_history.quantity,
    sales_history.sale_date
FROM sales_history
INNER JOIN products
    ON products.product_id = sales_history.product_id
WHERE sales_history.partner_id = ?
ORDER BY sales_history.sale_date, sales_history.sale_id
"""


def format_sale_date(value) -> str:
    text = str(value)[:10]
    try:
        return datetime.strptime(text, "%Y-%m-%d").strftime("%d.%m.%Y")
    except ValueError:
        return text


def list_partners(connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        rows = connection.execute(
            """
            SELECT partner_id, company_name, phone, rating
            FROM partners
            ORDER BY partner_id
            """
        ).fetchall()
        return [
            {
                "partner_id": row["partner_id"],
                "company_name": row["company_name"],
                "phone": row["phone"] or "—",
                "rating": "—" if row["rating"] is None else str(row["rating"]).rstrip("0").rstrip("."),
            }
            for row in rows
        ]
    finally:
        if own:
            connection.close()


def get_partner(partner_id, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        row = connection.execute(
            "SELECT partner_id, company_name FROM partners WHERE partner_id = ?",
            (partner_id,),
        ).fetchone()
        if row is None:
            return None
        return {"partner_id": row["partner_id"], "company_name": row["company_name"]}
    finally:
        if own:
            connection.close()


def load_shipments(partner_id, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        rows = connection.execute(HISTORY_SQL, (partner_id,)).fetchall()
        return [
            {
                "product_name": row["product_name"],
                "quantity": int(row["quantity"]),
                "sale_date": format_sale_date(row["sale_date"]),
            }
            for row in rows
        ]
    finally:
        if own:
            connection.close()
