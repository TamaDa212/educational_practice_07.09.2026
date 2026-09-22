from data import load_partner_card
from navigation import EDIT, LIST, PARTNER, Navigator
from partner_edit import (
    EMAIL_HINT,
    EMAIL_PLACEHOLDER,
    PARTNER_TYPES,
    PHONE_HINT,
    PHONE_PLACEHOLDER,
    PartnerEditWindow,
    parse_rating,
    validate,
    values_from_partner,
    values_from_post,
)
from screens import render_screen


def test_combo_is_strict_dropdown():
    html = PartnerEditWindow().render_form()
    assert "<select name=\"partner_type\"" in html
    assert 'data-window="PartnerEditWindow"' in html
    for item in ("ЗАО", "ООО", "ИП"):
        assert f'value="{item}"' in html
    assert '<input type="text" name="partner_type"' not in html


def test_phone_and_email_have_placeholders_and_tooltips():
    html = PartnerEditWindow().render_form()
    assert f'placeholder="{PHONE_PLACEHOLDER}"' in html
    assert f'title="{PHONE_HINT}"' in html
    assert f'placeholder="{EMAIL_PLACEHOLDER}"' in html
    assert f'title="{EMAIL_HINT}"' in html
    assert 'type="tel"' in html
    assert 'type="email"' in html


def test_rating_is_non_negative_integer_input():
    html = PartnerEditWindow().render_form()
    assert 'name="rating"' in html
    assert 'type="number"' in html
    assert 'min="0"' in html
    assert 'step="1"' in html
    assert parse_rating("-1") is None
    assert parse_rating("4.8") == "4"
    assert parse_rating("0") == "0"


def test_edit_form_receives_partner_id():
    partner = load_partner_card(4)
    window = PartnerEditWindow(4, values_from_partner(partner))
    html = window.render_form()
    assert 'name="partner_id" value="4"' in html
    assert "Новый Контур" in html
    assert "selected>ООО</option>" in html
    assert "Кузнецова А.Н." in html
    assert "hello@newcontour.ru" in html


def test_validate_rejects_free_type_and_negative_rating():
    errors = validate(
        values_from_post(
            {
                "company_name": ["Тест"],
                "partner_type": ["холдинг"],
                "rating": ["-3"],
                "address": [""],
                "director": [""],
                "phone": [""],
                "email": [""],
            }
        )
    )
    assert "partner_type" in errors
    assert "rating" in errors


def test_navigator_passes_id_into_edit_window():
    nav = Navigator()
    nav.open_edit(4)
    assert nav.screen == EDIT
    assert nav.params["partner_id"] == 4
    assert nav.selected_partner_id == 4
    html = render_screen(
        EDIT,
        nav.params,
        window=PartnerEditWindow(4, values_from_partner(load_partner_card(4))),
        trail=nav.trail(),
    )
    assert "PartnerEditWindow" in html
    assert 'value="4"' in html
    nav.back()
    assert nav.screen == PARTNER
    nav.back()
    assert nav.screen == LIST
    assert nav.selected_partner_id == 4


def test_add_form_has_empty_id():
    nav = Navigator()
    nav.open_edit(None)
    html = render_screen(
        EDIT, nav.params, window=PartnerEditWindow(), trail=nav.trail()
    )
    assert "CRM: Добавление партнера" in html
    assert 'name="partner_id" value=""' in html
    assert "Наименование" in html
    assert "Адрес" in html
    assert "ФИО директора" in html
    assert PARTNER_TYPES[0] == "ЗАО"
