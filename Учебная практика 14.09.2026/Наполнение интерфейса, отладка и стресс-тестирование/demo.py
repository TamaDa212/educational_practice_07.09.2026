from catalog import load_cards, raw_sales_sum
from db import get_connection, initialize_database
from page import render_page
from partner_service import list_partners_with_discount, quantity_or_zero


def run_demo():
    connection = get_connection(":memory:")
    initialize_database(connection)
    partners = list_partners_with_discount(connection)
    cards = load_cards(connection)
    html = render_page(cards)

    assert len(partners) == 5
    assert len(cards) == 5

    empty_partner = next(item for item in partners if item["partner_id"] == 4)
    empty_card = next(item for item in cards if item["partner_id"] == 4)
    raw_sum = raw_sales_sum(connection, 4)

    assert raw_sum is None
    assert quantity_or_zero(raw_sum) == 0
    assert empty_partner["total_quantity"] == 0
    assert empty_partner["discount_percent"] == 0
    assert empty_card["discount_percent"] == 0
    assert "Новый Контур" in html
    assert ">0%</div>" in html or "0%" in html

    opt = next(item for item in cards if item["partner_id"] == 5)
    assert opt["discount_percent"] == 5
    assert "opt@optmarket.ru" in html

    print("partner_id | company_name | phone | email | qty | discount")
    for partner in partners:
        phone = partner["phone"] or "—"
        print(
            f"{partner['partner_id']} | {partner['company_name']} | "
            f"{phone} | {partner['contact_email']} | "
            f"{partner['total_quantity']} | {partner['discount_percent']}%"
        )
    print("demo ok")
    connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(run_demo())
