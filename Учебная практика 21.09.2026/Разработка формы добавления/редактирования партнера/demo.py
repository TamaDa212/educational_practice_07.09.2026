from data import load_partner_card
from navigation import EDIT, LIST, Navigator
from partner_edit import PartnerEditWindow, values_from_partner, values_from_post, validate
from screens import render_screen


def run_demo():
    nav = Navigator()
    nav.open_edit(None)
    add_html = render_screen(EDIT, nav.params, window=PartnerEditWindow(), trail=nav.trail())
    assert "CRM: Добавление партнера" in add_html
    assert "<select name=\"partner_type\"" in add_html
    assert 'placeholder="+7 (999) 123-45-67"' in add_html
    assert 'placeholder="name@company.ru"' in add_html

    nav.open_edit(4)
    partner = load_partner_card(4)
    window = PartnerEditWindow(4, values_from_partner(partner))
    edit_html = render_screen(EDIT, nav.params, window=window, trail=nav.trail())
    assert 'name="partner_id" value="4"' in edit_html
    assert "Новый Контур" in edit_html
    assert "ООО" in edit_html

    bad = validate(values_from_post({"company_name": ["А"], "partner_type": ["ООО"], "rating": ["-1"]}))
    assert "rating" in bad

    nav.back()
    nav.back()
    assert nav.screen == LIST
    assert nav.selected_partner_id == 4
    print("demo ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_demo())
