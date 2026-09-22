from messagebox import MessageBox
from partner_edit import PartnerEditWindow, values_from_partner
from validation import RATING_HINT, ValidationError, validate_partner


def run_demo():
    try:
        validate_partner(
            {
                "company_name": "Тест",
                "partner_type": "ООО",
                "email": "a@b.ru",
                "rating": "3,14",
            }
        )
        raise SystemExit("rating should fail")
    except ValidationError as exc:
        html = MessageBox.error(exc.message).render()
        assert "Ошибка" in html
        assert "крестик" in html
        assert RATING_HINT in html

    try:
        validate_partner(
            {
                "company_name": "",
                "partner_type": "ООО",
                "email": "",
                "rating": "",
            }
        )
        raise SystemExit("required should fail")
    except ValidationError as exc:
        assert "пустым" in exc.message

    info = MessageBox.information("Партнёр успешно добавлен в базу данных.").render()
    assert "Информация" in info
    assert "инфо-значок" in info

    warning = MessageBox.warning("Несохранённые данные будут потеряны.").render()
    assert "Предупреждение" in warning
    assert "восклицательный знак" in warning

    form = PartnerEditWindow().render_form()
    assert "unsaved-warning" in form
    assert values_from_partner(None)["company_name"] == ""
    print("demo ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_demo())
