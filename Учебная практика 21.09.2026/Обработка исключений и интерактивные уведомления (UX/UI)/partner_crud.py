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
DISCOUNT_DIR = (
    ROOT
    / "Учебная практика 14.09.2026"
    / "Разработка ядра бизнес-логики (Расчет скидки)"
)
sys.path.insert(0, str(DISCOUNT_DIR))
sys.path.insert(0, str(HERE))

from partner_discount import calculate_partner_discount

from db import open_db

LIST_SQL = """
SELECT
    partners.partner_id,
    partners.partner_type,
    partners.company_name,
    partners.inn,
    partners.director,
    partners.address,
    partners.contact_email,
    partners.phone,
    partners.rating,
    COALESCE(SUM(sales_history.quantity), 0) AS total_quantity
FROM partners
LEFT JOIN sales_history
    ON sales_history.partner_id = partners.partner_id
GROUP BY
    partners.partner_id,
    partners.partner_type,
    partners.company_name,
    partners.inn,
    partners.director,
    partners.address,
    partners.contact_email,
    partners.phone,
    partners.rating
ORDER BY partners.partner_id
"""

GET_SQL = """
SELECT
    partners.partner_id,
    partners.partner_type,
    partners.company_name,
    partners.inn,
    partners.director,
    partners.address,
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
    partners.partner_type,
    partners.company_name,
    partners.inn,
    partners.director,
    partners.address,
    partners.contact_email,
    partners.phone,
    partners.rating
"""

INSERT_SQL = """
INSERT INTO partners (
    partner_id, partner_type, company_name, inn, director, address,
    contact_email, phone, rating
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

UPDATE_SQL = """
UPDATE partners
SET partner_type = ?,
    company_name = ?,
    director = ?,
    address = ?,
    contact_email = ?,
    phone = ?,
    rating = ?
WHERE partner_id = ?
"""


class IntegrityError(Exception):
    pass


def _blank(value):
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _rating(value):
    if value is None or value == "":
        return None
    return int(value)


def row_to_partner(row):
    if row is None:
        return None
    total_quantity = int(row["total_quantity"] or 0)
    rating = row["rating"]
    return {
        "partner_id": row["partner_id"],
        "partner_type": row["partner_type"],
        "company_name": row["company_name"],
        "inn": row["inn"],
        "director": row["director"] or "",
        "address": row["address"] or "",
        "contact_email": row["contact_email"],
        "email": row["contact_email"],
        "phone": row["phone"] or "",
        "rating": "" if rating is None else str(int(rating)),
        "total_quantity": total_quantity,
        "discount_percent": calculate_partner_discount(total_quantity),
    }


def partner_exists(connection, partner_id):
    row = connection.execute(
        "SELECT 1 FROM partners WHERE partner_id = ?", (partner_id,)
    ).fetchone()
    return row is not None


def sales_count(connection, partner_id):
    row = connection.execute(
        "SELECT COUNT(*) AS n FROM sales_history WHERE partner_id = ?",
        (partner_id,),
    ).fetchone()
    return int(row["n"])


def next_partner_id(connection):
    row = connection.execute("SELECT COALESCE(MAX(partner_id), 0) + 1 AS n FROM partners").fetchone()
    return int(row["n"])


def unique_inn(connection, partner_id):
    inn = f"{9000000000 + int(partner_id):012d}"[-12:]
    while connection.execute("SELECT 1 FROM partners WHERE inn = ?", (inn,)).fetchone():
        partner_id += 1
        inn = f"{9000000000 + int(partner_id):012d}"[-12:]
    return inn


def list_partners(connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        return [row_to_partner(row) for row in connection.execute(LIST_SQL)]
    finally:
        if own:
            connection.close()


def get_partner(partner_id, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        row = connection.execute(GET_SQL, (partner_id,)).fetchone()
        return row_to_partner(row)
    finally:
        if own:
            connection.close()


def insert_partner(values, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        partner_id = next_partner_id(connection)
        # Новый id не пересекается с существующими PK и FK истории продаж.
        inn = unique_inn(connection, partner_id)
        connection.execute(
            INSERT_SQL,
            (
                partner_id,
                values["partner_type"],
                values["company_name"],
                inn,
                _blank(values.get("director")),
                _blank(values.get("address")),
                values.get("email") or values.get("contact_email") or "",
                _blank(values.get("phone")),
                _rating(values.get("rating")),
            ),
        )
        connection.commit()
        return get_partner(partner_id, connection)
    finally:
        if own:
            connection.close()


def update_partner(partner_id, values, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        # UPDATE только существующих строк: PK и ссылки sales_history не трогаем.
        if not partner_exists(connection, partner_id):
            raise IntegrityError(f"Партнер № {partner_id} не найден, UPDATE отменён.")
        cursor = connection.execute(
            UPDATE_SQL,
            (
                values["partner_type"],
                values["company_name"],
                _blank(values.get("director")),
                _blank(values.get("address")),
                values.get("email") or values.get("contact_email") or "",
                _blank(values.get("phone")),
                _rating(values.get("rating")),
                partner_id,
            ),
        )
        if cursor.rowcount != 1:
            raise IntegrityError(f"Партнер № {partner_id} не обновлён.")
        connection.commit()
        return get_partner(partner_id, connection)
    finally:
        if own:
            connection.close()


def save_partner(partner_id, values, connection=None):
    if partner_id is None:
        return insert_partner(values, connection)
    return update_partner(partner_id, values, connection)


def delete_partner(partner_id, connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        if not partner_exists(connection, partner_id):
            raise IntegrityError(f"Партнер № {partner_id} не найден.")
        if sales_count(connection, partner_id) > 0:
            raise IntegrityError("Нельзя удалить партнёра: есть история продаж.")
        connection.execute("DELETE FROM partners WHERE partner_id = ?", (partner_id,))
        connection.commit()
    finally:
        if own:
            connection.close()
