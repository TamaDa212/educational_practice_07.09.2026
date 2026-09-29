from history_window import PartnerHistoryWindow
from sales_history import HISTORY_SQL, format_sale_date, get_partner, load_shipments
from screens import render_history, render_list
from db import open_db


def test_join_returns_product_quantity_and_human_date(tmp_path):
    connection = open_db(tmp_path / "p.db")
    assert "INNER JOIN products" in HISTORY_SQL
    rows = load_shipments(1, connection)
    assert rows == [
        {
            "product_name": 'Стиральный порошок "Альфа"',
            "quantity": 50,
            "sale_date": "01.03.2026",
        },
        {
            "product_name": "Кондиционер для белья",
            "quantity": 30,
            "sale_date": "20.03.2026",
        },
    ]
    assert format_sale_date("2026-04-01") == "01.04.2026"
    connection.close()


def test_history_window_uses_style_and_partner_name(tmp_path):
    connection = open_db(tmp_path / "p.db")
    partner = get_partner(5, connection)
    window = PartnerHistoryWindow(partner, load_shipments(5, connection))
    html = render_history(window)
    assert window.title == 'CRM: История реализации продукции — ТД "ОптМаркет"'
    assert "PartnerHistoryWindow" in html
    assert 'data-partner-id="5"' in html
    assert "/resources/company_logo.png" in html
    assert "/resources/app_icon.png" in html
    assert "/static/style.css" in html
    assert "Наименование продукции" in html
    assert "Количество (шт.)" in html
    assert "Дата продажи" in html
    assert "01.04.2026" in html
    assert "10000" in html
    connection.close()


def test_main_form_passes_selected_partner_to_history():
    html = render_list(
        [{"partner_id": 1, "company_name": 'ООО "Логистик-Экспресс"', "phone": "—", "rating": "4.8"}],
        1,
    )
    assert 'href="/partner/1"' in html
    assert 'href="/partner/1/history"' in html
    assert "История продаж" in html
    assert "selected" in html


def test_partner_without_shipments_does_not_crash(tmp_path):
    connection = open_db(tmp_path / "p.db")
    partner = get_partner(4, connection)
    html = render_history(PartnerHistoryWindow(partner, load_shipments(4, connection)))
    assert "Отгрузок по этому партнеру нет" in html
    assert "Новый Контур" in html
    connection.close()
