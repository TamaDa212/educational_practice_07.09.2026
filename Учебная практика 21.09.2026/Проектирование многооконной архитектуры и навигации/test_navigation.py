from navigation import HISTORY, LIST, MISSING, PARTNER, Navigator, parse_partner_id


def test_parse_partner_id_does_not_raise():
    assert parse_partner_id(4) == 4
    assert parse_partner_id("5") == 5
    assert parse_partner_id("abc") is None
    assert parse_partner_id(None) is None
    assert parse_partner_id("-1") is None


def test_back_on_list_keeps_app_running():
    nav = Navigator()
    assert nav.back() == (LIST, {})
    assert nav.screen == LIST


def test_partner_then_back_keeps_selected_id():
    nav = Navigator()
    nav.open_partner(4)
    assert nav.screen == PARTNER
    assert nav.selected_partner_id == 4
    nav.back()
    assert nav.screen == LIST
    assert nav.selected_partner_id == 4


def test_history_stack_and_back():
    nav = Navigator()
    nav.open_history(5)
    assert [item[0] for item in nav.stack] == [LIST, PARTNER, HISTORY]
    nav.back()
    assert nav.screen == PARTNER
    nav.back()
    assert nav.screen == LIST


def test_invalid_partner_opens_missing_screen():
    nav = Navigator()
    nav.open_partner("нет")
    assert nav.screen == MISSING
    nav.back()
    assert nav.screen == LIST
