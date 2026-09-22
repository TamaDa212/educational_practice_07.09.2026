from messagebox import ERROR, INFORMATION, WARNING, ICON_LABELS, TITLES, MessageBox
from partner_edit import PartnerEditWindow, UNSAVED_WARNING, empty_values
from validation import (
    EMAIL_HINT,
    NAME_HINT,
    RATING_HINT,
    ValidationError,
    check_rating,
    check_required_email,
    check_required_name,
    validate_partner,
)


def valid_values(**overrides):
    data = empty_values()
    data.update(
        {
            "company_name": "Северная звезда",
            "partner_type": "ЗАО",
            "email": "star@alliance.ru",
            "rating": "3",
        }
    )
    data.update(overrides)
    return data


def test_rating_rejects_punctuation_via_try_except():
    try:
        check_rating("4.8")
        assert False, "expected ValidationError"
    except ValidationError as exc:
        assert exc.message == RATING_HINT
        assert "знаки препинания" in exc.message


def test_rating_rejects_negative_without_crash():
    try:
        check_rating("-2")
        assert False, "expected ValidationError"
    except ValidationError as exc:
        assert "отрицательным" in exc.message


def test_required_name_and_email():
    try:
        check_required_name("  ")
        assert False
    except ValidationError as exc:
        assert exc.message == NAME_HINT
    try:
        check_required_email("")
        assert False
    except ValidationError as exc:
        assert exc.message == EMAIL_HINT


def test_validate_partner_passes_clean_integer_rating():
    cleaned = validate_partner(valid_values(rating="4"))
    assert cleaned["rating"] == "4"


def test_error_warning_information_have_title_and_icon():
    error = MessageBox.error(RATING_HINT).render()
    assert f'data-kind="{ERROR}"' in error
    assert f">{TITLES[ERROR]}<" in error
    assert f'aria-label="{ICON_LABELS[ERROR]}"' in error
    assert RATING_HINT in error
    assert "message-box-overlay" in error

    warning = MessageBox.warning(UNSAVED_WARNING).render("unsaved-warning")
    assert f'data-kind="{WARNING}"' in warning
    assert f">{TITLES[WARNING]}<" in warning
    assert f'aria-label="{ICON_LABELS[WARNING]}"' in warning
    assert "Да" in warning
    assert "Нет" in warning

    info = MessageBox.information("Партнёр успешно добавлен в базу данных.").render()
    assert f'data-kind="{INFORMATION}"' in info
    assert f">{TITLES[INFORMATION]}<" in info
    assert f'aria-label="{ICON_LABELS[INFORMATION]}"' in info


def test_form_contains_warning_dialog_and_cancel():
    html = PartnerEditWindow().render_form()
    assert 'id="unsaved-warning"' in html
    assert "Предупреждение" in html
    assert "Отмена" in html
    assert "Назад" in html
    assert "js-cancel" in html


def test_invalid_save_payload_does_not_raise_out():
    try:
        validate_partner(valid_values(company_name="", rating="1,5"))
    except ValidationError as exc:
        assert "пустым" in exc.message or "целым" in exc.message
    else:
        assert False
