from html import escape

from navigation import EDIT, LIST, MISSING
from partner_edit import PartnerEditWindow


def shell(title, trail, body, actions="", dialog=None):
    crumbs = " → ".join(escape(item) for item in trail)
    dialog_html = dialog.render() if dialog else ""
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="icon" href="/resources/app_icon.png" type="image/png">
  <link rel="stylesheet" href="/static/style.css">
  <link rel="stylesheet" href="/static/form.css">
  <link rel="stylesheet" href="/static/dialog.css?v=3">
  <script src="/static/dialogs.js?v=3" defer></script>
</head>
<body>
  <main class="window">
    <div class="window-bar">
      <img src="/resources/app_icon.png" alt="Иконка приложения">
      <span>{escape(title)}</span>
    </div>
    <header class="header">
      <img src="/resources/company_logo.png" alt="Логотип компании Альянс">
      <h1>{escape(title)}</h1>
    </header>
    <p class="trail">{crumbs}</p>
    {body}
    {f'<div class="actions">{actions}</div>' if actions else ""}
  </main>
  {dialog_html}
</body>
</html>
"""


def format_discount(value) -> str:
    if value is None:
        return "0%"
    try:
        return f"{int(value)}%"
    except (TypeError, ValueError):
        return "0%"


def render_list(partners, selected_partner_id, trail, dialog=None):
    rows = []
    for partner in partners:
        selected = " selected" if partner["partner_id"] == selected_partner_id else ""
        href = f"/partner/{partner['partner_id']}/edit"
        rows.append(
            f"""
            <tr class="partner-row{selected}" data-href="{href}"
                onclick="location.href=this.dataset.href"
                ondblclick="location.href=this.dataset.href">
              <td>{escape(str(partner['partner_type']))}</td>
              <td>{escape(str(partner['company_name']))}</td>
              <td>{escape(str(partner.get('director') or '—'))}</td>
              <td>{escape(str(partner.get('phone') or '—'))}</td>
              <td>{escape(str(partner.get('rating') or '—'))}</td>
              <td>{format_discount(partner.get('discount_percent'))}</td>
            </tr>
            """
        )
    body = f"""
    <section class="board" aria-label="Таблица партнеров">
      <table class="partners">
        <thead>
          <tr>
            <th>Тип</th>
            <th>Наименование</th>
            <th>Директор</th>
            <th>Телефон</th>
            <th>Рейтинг</th>
            <th>Скидка</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows)}
        </tbody>
      </table>
    </section>
    """
    actions = (
        '<a class="btn" href="/partner/new">Добавить</a>'
        '<a class="btn" href="/">Обновить</a>'
    )
    return shell("CRM: Список партнеров и скидок", trail, body, actions, dialog=dialog)


def render_edit(window: PartnerEditWindow, trail):
    body = f'<section class="board">{window.render_form()}</section>'
    return shell(window.title(), trail, body)


def render_missing(partner_id, trail, dialog=None):
    body = (
        '<section class="board">'
        f"<p class='empty'>Партнер № {escape(str(partner_id))} не найден. "
        "Приложение продолжает работу.</p>"
        "</section>"
    )
    actions = '<a class="btn" href="/">К списку</a>'
    return shell("CRM: Партнер не найден", trail, body, actions, dialog=dialog)


def render_screen(
    screen,
    params,
    *,
    partners=None,
    window=None,
    selected_partner_id=None,
    trail=None,
    dialog=None,
):
    trail = trail or []
    if screen == LIST:
        return render_list(partners or [], selected_partner_id, trail, dialog=dialog)
    if screen == EDIT:
        return render_edit(window, trail)
    if screen == MISSING:
        return render_missing(params.get("partner_id"), trail, dialog=dialog)
    return render_list(partners or [], selected_partner_id, trail, dialog=dialog)
