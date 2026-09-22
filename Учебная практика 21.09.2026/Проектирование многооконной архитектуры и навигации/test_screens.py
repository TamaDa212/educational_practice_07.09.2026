from data import load_partner_card, load_sales
from navigation import HISTORY, LIST, PARTNER, Navigator
from screens import render_screen


def test_unknown_partner_returns_none():
    assert load_partner_card(999) is None


def test_partner_without_sales_has_empty_history():
    partner = load_partner_card(4)
    sales = load_sales(4)
    assert partner["discount_percent"] == 0
    assert sales == []
    html = render_screen(
        HISTORY,
        {"partner_id": 4},
        partner=partner,
        sales=sales,
        trail=["Список партнеров", "Карточка партнера", "История продаж"],
    )
    assert "Истории продаж нет" in html
    assert partner["discount_percent"] == 0


def test_list_html_marks_selected_partner():
    from catalog import load_cards

    nav = Navigator()
    nav.open_partner(1)
    nav.back()
    html = render_screen(
        LIST,
        {},
        partners=load_cards(),
        selected_partner_id=nav.selected_partner_id,
        trail=nav.trail(),
    )
    assert 'href="/partner/1"' in html
    assert "selected" in html
    assert "CRM: Список партнеров и скидок" in html


def test_partner_screen_has_history_link():
    partner = load_partner_card(5)
    html = render_screen(
        PARTNER,
        {"partner_id": 5},
        partner=partner,
        trail=["Список партнеров", "Карточка партнера"],
    )
    assert "История продаж" in html
    assert "opt@optmarket.ru" in html
    assert "5%" in html
