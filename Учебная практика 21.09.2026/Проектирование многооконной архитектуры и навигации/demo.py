from data import load_partner_card, load_sales
from navigation import LIST, Navigator
from screens import render_screen
from catalog import load_cards


def run_demo():
    nav = Navigator()
    cards = load_cards()
    assert len(cards) == 5

    nav.open_partner(4)
    partner = load_partner_card(4)
    assert partner is not None
    assert partner["discount_percent"] == 0
    html = render_screen(nav.screen, nav.params, partner=partner, trail=nav.trail())
    assert "Новый Контур" in html

    nav.open_history(4)
    sales = load_sales(4)
    assert sales == []
    html = render_screen(
        nav.screen, nav.params, partner=partner, sales=sales, trail=nav.trail()
    )
    assert "Истории продаж нет" in html

    nav.back()
    nav.back()
    assert nav.screen == LIST
    assert nav.selected_partner_id == 4

    nav.open_partner("abc")
    assert nav.screen == "missing"
    nav.back()
    assert nav.screen == LIST

    html = render_screen(
        LIST, {}, partners=cards, selected_partner_id=nav.selected_partner_id, trail=nav.trail()
    )
    assert "selected" in html
    print("demo ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_demo())
