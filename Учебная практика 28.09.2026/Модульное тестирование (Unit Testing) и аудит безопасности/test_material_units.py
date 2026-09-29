import math

import core_path  # noqa: F401

from db import open_db
from material_calculator import calculate_material_amount


def test_01_standard_calculation(tmp_path):
    connection = open_db(tmp_path / "materials.db")
    # 10 × 10 × 1.5 × 2 × 1.01 = 303 ровно.
    amount = calculate_material_amount(3, 3, 2, 10, 10, connection)
    assert amount == 303
    connection.close()


def test_02_fraction_rounds_up(tmp_path):
    connection = open_db(tmp_path / "materials.db")
    # 2 × 3 × 1.5 × 4 × 1.01 = 36.36, ceil даёт 37, а не 36.
    raw = 2 * 3 * 1.5 * 4 * 1.01
    amount = calculate_material_amount(3, 3, 4, 2, 3, connection)
    assert raw == 36.36
    assert amount == math.ceil(raw)
    assert amount == 37
    connection.close()


def test_03_unknown_type_returns_minus_one(tmp_path):
    connection = open_db(tmp_path / "materials.db")
    assert calculate_material_amount(99, 1, 2, 1, 1, connection) == -1
    assert calculate_material_amount(1, 99, 2, 1, 1, connection) == -1
    connection.close()


def test_04_negative_params_return_minus_one(tmp_path):
    connection = open_db(tmp_path / "materials.db")
    assert calculate_material_amount(1, 1, 2, -1, 2, connection) == -1
    assert calculate_material_amount(1, 1, 2, 2, -5, connection) == -1
    connection.close()


def test_05_zero_or_negative_quantity_returns_minus_one(tmp_path):
    connection = open_db(tmp_path / "materials.db")
    assert calculate_material_amount(1, 1, 0, 1, 1, connection) == -1
    assert calculate_material_amount(1, 1, -3, 1, 1, connection) == -1
    connection.close()
