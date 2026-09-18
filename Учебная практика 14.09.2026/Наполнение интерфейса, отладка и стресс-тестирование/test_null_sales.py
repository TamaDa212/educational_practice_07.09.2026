from catalog import discount_or_zero, load_cards, raw_sales_sum
from db import get_connection, initialize_database
from page import format_discount, render_page
from partner_service import quantity_or_zero


def setup_memory_db():
    connection = get_connection(":memory:")
    initialize_database(connection)
    return connection


def test_quantity_none_and_zero_are_safe():
    assert quantity_or_zero(None) == 0
    assert quantity_or_zero(0) == 0
    assert quantity_or_zero("12") == 12
    assert quantity_or_zero("not-a-number") == 0
    assert discount_or_zero(None, 0) == 0
    assert discount_or_zero(None, 10000) == 5
    assert format_discount(None) == "0%"
    assert format_discount("bad") == "0%"


def test_partner_without_sales_raw_sum_is_null():
    connection = setup_memory_db()
    raw_sum = raw_sales_sum(connection, 4)
    cards = load_cards(connection)
    connection.close()
    assert raw_sum is None
    empty = next(item for item in cards if item["partner_id"] == 4)
    assert empty["total_quantity"] == 0
    assert empty["discount_percent"] == 0
    html = render_page(cards)
    assert "Новый Контур" in html
    assert "0%" in html


def test_ui_uses_backend_contacts_and_discount():
    connection = setup_memory_db()
    cards = load_cards(connection)
    connection.close()
    opt = next(item for item in cards if item["partner_id"] == 5)
    assert opt["contact_email"] == "opt@optmarket.ru"
    assert opt["phone"] == "+7 (812) 300-40-50"
    assert opt["discount_percent"] == 5
    logex = next(item for item in cards if item["partner_id"] == 1)
    assert logex["discount_percent"] == 0
    assert logex["contact_email"] == "info@logex.ru"
