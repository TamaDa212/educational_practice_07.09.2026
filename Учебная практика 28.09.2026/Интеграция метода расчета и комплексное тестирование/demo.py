from form_page import render_calculator
from order_calculator import calculate_order


def run_demo():
    ok = calculate_order("3", "3", "4", "2", "3")
    assert ok["amount"] == 37
    html = render_calculator(
        {
            "product_type_id": "3",
            "material_type_id": "3",
            "quantity": "4",
            "param_1": "2",
            "param_2": "3",
        },
        ok,
    )
    assert "37" in html
    bad = calculate_order("3", "3", "4", "-1", "2")
    assert bad["amount"] == -1
    missing = calculate_order("50", "1", "1", "1", "1")
    assert missing["amount"] == -1
    assert "Расчет не выполнен" in missing["message"]
    print("demo ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_demo())
