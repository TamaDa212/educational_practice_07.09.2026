from form_page import render_calculator
from order_calculator import ERROR_MESSAGE, calculate_order


def test_form_shows_material_amount():
    result = calculate_order(3, 3, 4, 2, 3)
    assert result["ok"] is True
    assert result["amount"] == 37
    html = render_calculator(
        {
            "product_type_id": "3",
            "material_type_id": "3",
            "quantity": "4",
            "param_1": "2",
            "param_2": "3",
        },
        result,
    )
    assert "Необходимо сырья: 37 ед." in html
    assert "Калькулятор заказа" in html


def test_negative_size_shows_error_instead_of_crash():
    result = calculate_order(3, 3, 4, -2, 3)
    assert result["amount"] == -1
    assert result["ok"] is False
    html = render_calculator(
        {
            "product_type_id": "3",
            "material_type_id": "3",
            "quantity": "4",
            "param_1": "-2",
            "param_2": "3",
        },
        result,
    )
    assert ERROR_MESSAGE in html
    assert "Traceback" not in html


def test_unknown_type_id_shows_error_instead_of_crash():
    result = calculate_order(99, 1, 2, 1.5, 2)
    assert result["amount"] == -1
    html = render_calculator(
        {
            "product_type_id": "99",
            "material_type_id": "1",
            "quantity": "2",
            "param_1": "1.5",
            "param_2": "2",
        },
        result,
    )
    assert "Расчет не выполнен" in html
    assert "существующие ID" in html


def test_zero_quantity_shows_error():
    result = calculate_order(1, 1, 0, 1, 1)
    assert result == {"ok": False, "amount": -1, "message": ERROR_MESSAGE}
