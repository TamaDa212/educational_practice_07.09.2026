from html import escape

from navigation import parse_partner_id

# ComboBox только из справочника ТЗ — свободный ввод типа запрещён.
PARTNER_TYPES = ("ЗАО", "ООО", "ИП", "ТК", "ТД", "ПАО", "ОАО", "АО")

PHONE_PLACEHOLDER = "+7 (999) 123-45-67"
PHONE_HINT = "Формат телефона: +7 (XXX) XXX-XX-XX"
EMAIL_PLACEHOLDER = "name@company.ru"
EMAIL_HINT = "Формат email: имя@домен, например name@company.ru"

FIELDS = (
    "company_name",
    "partner_type",
    "rating",
    "address",
    "director",
    "phone",
    "email",
)


def empty_values():
    return {name: "" for name in FIELDS}


def parse_rating(value):
    if value is None or value == "" or value == "—":
        return ""
    try:
        number = int(value)
    except (TypeError, ValueError):
        try:
            number = int(float(str(value).replace(",", ".")))
        except (TypeError, ValueError):
            return None
    if number < 0:
        return None
    return str(number)


def values_from_partner(partner):
    values = empty_values()
    if not partner:
        return values
    values["company_name"] = partner.get("company_name") or ""
    values["partner_type"] = partner.get("partner_type") or ""
    rating = parse_rating(partner.get("rating"))
    values["rating"] = "" if rating is None else rating
    values["address"] = partner.get("address") or ""
    director = partner.get("director") or ""
    values["director"] = "" if director in {"", "—"} else director
    phone = partner.get("phone") or ""
    values["phone"] = "" if phone in {"", "—"} else phone
    email = partner.get("contact_email") or partner.get("email") or ""
    values["email"] = "" if email in {"", "—"} else email
    return values


def values_from_post(fields):
    values = empty_values()
    for name in FIELDS:
        raw = fields.get(name, [""])
        values[name] = (raw[0] if raw else "").strip()
    return values


def validate(values):
    errors = {}
    if not values["company_name"]:
        errors["company_name"] = "Укажите наименование."
    if values["partner_type"] not in PARTNER_TYPES:
        errors["partner_type"] = "Тип партнера выбирается только из списка."
    rating = parse_rating(values["rating"])
    if values["rating"] != "" and rating is None:
        errors["rating"] = "Рейтинг — целое неотрицательное число."
    elif rating is not None:
        values["rating"] = rating
    if not values["email"]:
        errors["email"] = "Укажите email компании."
    return errors


class PartnerEditWindow:
    """Форма добавления и редактирования партнёра: текст, ComboBox, целое, маски связи."""

    def __init__(self, partner_id=None, values=None, errors=None, notice=None):
        self.partner_id = parse_partner_id(partner_id)
        self.values = values or empty_values()
        self.errors = errors or {}
        self.notice = notice or ""

    def is_create(self):
        return self.partner_id is None

    def title(self):
        if self.is_create():
            return "CRM: Добавление партнера"
        return "CRM: Редактирование партнера"

    def combo_options(self):
        selected = self.values.get("partner_type") or ""
        types = list(PARTNER_TYPES)
        if selected and selected not in types:
            types.append(selected)
        options = ['<option value="">Выберите тип</option>']
        for item in types:
            mark = " selected" if item == selected else ""
            options.append(f'<option value="{escape(item)}"{mark}>{escape(item)}</option>')
        return "\n".join(options)

    def field_error(self, name):
        message = self.errors.get(name)
        if not message:
            return ""
        return f'<p class="field-error">{escape(message)}</p>'

    def render_form(self):
        values = self.values
        # ID партнёра передаётся между окнами скрытым полем: POST знает INSERT это или UPDATE.
        hidden_id = "" if self.partner_id is None else str(self.partner_id)
        notice = (
            f'<p class="notice">{escape(self.notice)}</p>' if self.notice else ""
        )
        return f"""
        <form class="partner-form" data-window="PartnerEditWindow" method="post" action="/partner/save">
          <input type="hidden" name="partner_id" value="{escape(hidden_id)}">
          {notice}
          <label>
            Наименование
            <input type="text" name="company_name" value="{escape(values['company_name'])}" required>
            {self.field_error("company_name")}
          </label>
          <label>
            Тип партнера
            <select name="partner_type" required>
              {self.combo_options()}
            </select>
            {self.field_error("partner_type")}
          </label>
          <label>
            Рейтинг
            <input type="number" name="rating" min="0" step="1" inputmode="numeric"
                   value="{escape(values['rating'])}">
            {self.field_error("rating")}
          </label>
          <label>
            Адрес
            <input type="text" name="address" value="{escape(values['address'])}">
          </label>
          <label>
            ФИО директора
            <input type="text" name="director" value="{escape(values['director'])}">
          </label>
          <label>
            Телефон компании
            <input type="tel" name="phone" value="{escape(values['phone'])}"
                   placeholder="{PHONE_PLACEHOLDER}" title="{PHONE_HINT}"
                   aria-describedby="phone-hint">
            <span class="hint" id="phone-hint">{PHONE_HINT}</span>
          </label>
          <label>
            Email компании
            <input type="email" name="email" value="{escape(values['email'])}"
                   placeholder="{EMAIL_PLACEHOLDER}" title="{EMAIL_HINT}"
                   aria-describedby="email-hint">
            <span class="hint" id="email-hint">{EMAIL_HINT}</span>
          </label>
          <div class="form-actions">
            <button type="submit">Сохранить</button>
            <a class="btn" href="/">Закрыть</a>
          </div>
        </form>
        """
