from partner_edit import PARTNER_TYPES


class ValidationError(Exception):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.message = message
        self.field = field


RATING_HINT = (
    "Рейтинг должен быть целым числом от 0. "
    "Пожалуйста, удалите знаки препинания и повторите попытку."
)
NAME_HINT = (
    "Наименование не должно быть пустым. "
    "Заполните поле «Наименование» и нажмите «Сохранить»."
)
EMAIL_HINT = (
    "Email не должен быть пустым. "
    "Укажите адрес компании, например name@company.ru, и повторите попытку."
)
TYPE_HINT = (
    "Тип партнера выбирается только из списка. "
    "Откройте ComboBox, выберите значение и повторите сохранение."
)


def check_required_name(value):
    if not (value or "").strip():
        raise ValidationError(NAME_HINT, "company_name")
    return value.strip()


def check_required_email(value):
    if not (value or "").strip():
        raise ValidationError(EMAIL_HINT, "email")
    return value.strip()


def check_rating(value):
    text = "" if value is None else str(value).strip()
    if text == "":
        return None
    try:
        # int() отбрасывает дробную часть только у float; строка "4.8" должна упасть.
        if any(mark in text for mark in "., "):
            raise ValueError("punctuation")
        number = int(text)
    except (TypeError, ValueError):
        raise ValidationError(RATING_HINT, "rating") from None
    if number < 0:
        raise ValidationError(
            "Рейтинг не может быть отрицательным. Укажите целое число от 0 и повторите попытку.",
            "rating",
        )
    return number


def check_partner_type(value):
    if value not in PARTNER_TYPES:
        raise ValidationError(TYPE_HINT, "partner_type")
    return value


def validate_partner(values):
    """Проверка до записи в БД. Любая ошибка — ValidationError, без падения процесса."""
    try:
        check_required_name(values.get("company_name"))
        check_required_email(values.get("email"))
        check_partner_type(values.get("partner_type"))
        rating = check_rating(values.get("rating"))
    except ValidationError:
        raise
    except Exception:
        raise ValidationError(
            "Данные не прошли проверку. Исправьте поля формы и повторите попытку."
        ) from None
    cleaned = dict(values)
    cleaned["rating"] = "" if rating is None else str(rating)
    return cleaned
