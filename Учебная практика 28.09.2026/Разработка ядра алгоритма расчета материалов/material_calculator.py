import math

from db import open_db


def _as_int(value):
    if isinstance(value, bool) or isinstance(value, float):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _as_positive_float(value):
    if isinstance(value, bool):
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if number <= 0 or math.isnan(number) or math.isinf(number):
        return None
    return number


def calculate_material_amount(
    product_type_id,
    material_type_id,
    quantity,
    param_1,
    param_2,
    connection=None,
):
    """Расход сырья на партию. При ошибке входных данных или справочника возвращает -1."""
    product_type_id = _as_int(product_type_id)
    material_type_id = _as_int(material_type_id)
    quantity = _as_int(quantity)
    param_1 = _as_positive_float(param_1)
    param_2 = _as_positive_float(param_2)
    if None in (product_type_id, material_type_id, quantity, param_1, param_2):
        return -1
    if product_type_id <= 0 or material_type_id <= 0 or quantity <= 0:
        return -1

    own = connection is None
    if own:
        connection = open_db()
    try:
        product = connection.execute(
            "SELECT coefficient FROM product_types WHERE product_type_id = ?",
            (product_type_id,),
        ).fetchone()
        material = connection.execute(
            "SELECT defect_percent FROM material_types WHERE material_type_id = ?",
            (material_type_id,),
        ).fetchone()
        if product is None or material is None:
            return -1
        coefficient = float(product["coefficient"])
        defect_percent = float(material["defect_percent"])
        if coefficient <= 0 or defect_percent < 0:
            return -1
        per_unit = param_1 * param_2 * coefficient
        net = per_unit * quantity
        # Процент брака в справочнике задан как 0.8 для 0,8 %.
        total = net * (1 + defect_percent / 100)
        return math.ceil(total)
    except (TypeError, ValueError, ArithmeticError):
        return -1
    finally:
        if own:
            connection.close()
