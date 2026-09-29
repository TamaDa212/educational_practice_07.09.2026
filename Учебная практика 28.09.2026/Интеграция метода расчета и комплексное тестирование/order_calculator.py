import core_path  # noqa: F401

from db import open_db
from material_calculator import calculate_material_amount

ERROR_MESSAGE = (
    "Расчет не выполнен. Укажите существующие ID типа продукции и материала, "
    "количество больше 0 и положительные размеры продукции."
)


def list_product_types(connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        rows = connection.execute(
            "SELECT product_type_id, type_name, coefficient FROM product_types ORDER BY product_type_id"
        ).fetchall()
        items = []
        for row in rows:
            items.append(
                {
                    "product_type_id": row["product_type_id"],
                    "type_name": row["type_name"],
                    "coefficient": row["coefficient"],
                }
            )
        return items
    finally:
        if own:
            connection.close()


def list_material_types(connection=None):
    own = connection is None
    if own:
        connection = open_db()
    try:
        rows = connection.execute(
            "SELECT material_type_id, type_name, defect_percent FROM material_types ORDER BY material_type_id"
        ).fetchall()
        items = []
        for row in rows:
            items.append(
                {
                    "material_type_id": row["material_type_id"],
                    "type_name": row["type_name"],
                    "defect_percent": row["defect_percent"],
                }
            )
        return items
    finally:
        if own:
            connection.close()


def calculate_order(product_type_id, material_type_id, quantity, param_1, param_2):
    amount = calculate_material_amount(
        product_type_id,
        material_type_id,
        quantity,
        param_1,
        param_2,
    )
    # Ядро не бросает исключение: ошибка ввода и неизвестный ID приходят как -1.
    if amount == -1:
        return {"ok": False, "amount": -1, "message": ERROR_MESSAGE}
    return {
        "ok": True,
        "amount": amount,
        "message": f"Необходимо сырья: {amount} ед.",
    }
