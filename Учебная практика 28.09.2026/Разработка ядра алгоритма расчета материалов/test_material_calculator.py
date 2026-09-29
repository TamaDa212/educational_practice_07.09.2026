import math

from db import open_db
from material_calculator import calculate_material_amount


def test_rounds_up_with_coefficient_and_defect(tmp_path):
    connection = open_db(tmp_path / "m.db")
    # 2 × 3 × 1.5 = 9; × 4 = 36; × 1.01 = 36.36 → 37
    assert calculate_material_amount(3, 3, 4, 2, 3, connection) == 37
    connection.close()


def test_exact_integer_stays_without_extra_unit(tmp_path):
    connection = open_db(tmp_path / "m.db")
    # 2 × 2 × 2.35 = 9.4; × 10 = 94; брак 0 → не этот материал.
    # Ламинат 2.35, ДВП 0.8%: 1 × 1 × 2.35 × 1 × 1.008 = 2.3688 → 3
    assert calculate_material_amount(1, 1, 1, 1, 1, connection) == math.ceil(2.35 * 1.008)
    connection.close()


def test_unknown_ids_return_minus_one(tmp_path):
    connection = open_db(tmp_path / "m.db")
    assert calculate_material_amount(99, 1, 1, 1, 1, connection) == -1
    assert calculate_material_amount(1, 99, 1, 1, 1, connection) == -1
    connection.close()


def test_invalid_quantity_and_params_do_not_raise(tmp_path):
    connection = open_db(tmp_path / "m.db")
    assert calculate_material_amount(1, 1, 0, 1, 1, connection) == -1
    assert calculate_material_amount(1, 1, -5, 1, 1, connection) == -1
    assert calculate_material_amount(1, 1, 2, -1, 1, connection) == -1
    assert calculate_material_amount(1, 1, 2, 1, 0, connection) == -1
    assert calculate_material_amount(1, 1, 2, "нет", 1, connection) == -1
    connection.close()
