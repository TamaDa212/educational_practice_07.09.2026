from html import escape

from navigation import parse_partner_id
from messagebox import MessageBox

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

UNSAVED_WARNING = (
    "Есть несохранённые изменения. Если продолжить, данные будут безвозвратно потеряны. "
    "Нажмите «Да», чтобы закрыть карточку, или «Нет», чтобы остаться и сохранить."
)


def empty_values():
    return {name: "" for name in FIELDS}


def values_from_partner(partner):
    values = empty_values()
    if not partner:
        return values
    values["company_name"] = partner.get("company_name") or ""
    values["partner_type"] = partner.get("partner_type") or ""
    values["rating"] = "" if partner.get("rating") in (None, "—") else str(partner.get("rating"))
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


class PartnerEditWindow:
    def __init__(self, partner_id=None, values=None, dialog=None):
        self.partner_id = parse_partner_id(partner_id)
        self.values = values or empty_values()
        self.dialog = dialog

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

    def render_form(self):
        values = self.values
        hidden_id = "" if self.partner_id is None else str(self.partner_id)
        warning = MessageBox.warning(UNSAVED_WARNING)
        error_box = self.dialog.render() if self.dialog else ""
        return f"""
        <form class="partner-form" data-window="PartnerEditWindow" method="post"
              action="/partner/save" novalidate>
          <input type="hidden" name="partner_id" value="{escape(hidden_id)}">
          <label>
            Наименование
            <input type="text" name="company_name" value="{escape(values['company_name'])}">
          </label>
          <label>
            Тип партнера
            <select name="partner_type">
              {self.combo_options()}
            </select>
          </label>
          <label>
            Рейтинг
            <input type="text" name="rating" inputmode="numeric"
                   value="{escape(values['rating'])}">
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
                   placeholder="{PHONE_PLACEHOLDER}" title="{PHONE_HINT}">
            <span class="hint">{PHONE_HINT}</span>
          </label>
          <label>
            Email компании
            <input type="text" name="email" value="{escape(values['email'])}"
                   placeholder="{EMAIL_PLACEHOLDER}" title="{EMAIL_HINT}">
            <span class="hint">{EMAIL_HINT}</span>
          </label>
          <div class="form-actions">
            <button type="submit">Сохранить</button>
            <button type="button" class="btn js-cancel" data-href="/">Отмена</button>
            <a class="btn js-back" href="/">Назад</a>
          </div>
        </form>
        {warning.render("unsaved-warning")}
        {error_box}
        """
