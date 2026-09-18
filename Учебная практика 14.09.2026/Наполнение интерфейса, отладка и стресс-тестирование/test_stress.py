from catalog import load_cards
from db import get_connection, initialize_database
from page import render_page


def test_stress_many_partners_without_sales():
    connection = get_connection(":memory:")
    initialize_database(connection)
    extra = 250
    for partner_id in range(6, 6 + extra):
        connection.execute(
            """
            INSERT INTO partners (
                partner_id, company_name, inn, contact_email, phone, rating
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                partner_id,
                f'ООО "Стресс {partner_id}"',
                str(7700000000 + partner_id),
                f"stress{partner_id}@test.ru",
                None,
                None,
            ),
        )
    connection.commit()
    cards = load_cards(connection)
    html = render_page(cards)
    connection.close()

    assert len(cards) == 5 + extra
    empty_cards = [item for item in cards if item["partner_id"] >= 6]
    assert len(empty_cards) == extra
    assert all(item["discount_percent"] == 0 for item in empty_cards)
    assert all(item["phone"] == "—" for item in empty_cards)
    assert all(item["rating"] == "—" for item in empty_cards)
    assert html.count("0%") >= extra
    assert "TypeError" not in html
    assert "None" not in html


def test_stress_repeated_reload_does_not_raise():
    connection = get_connection(":memory:")
    initialize_database(connection)
    for _ in range(50):
        cards = load_cards(connection)
        html = render_page(cards)
        assert len(cards) == 5
        assert "CRM: Список партнеров и скидок" in html
    connection.close()
