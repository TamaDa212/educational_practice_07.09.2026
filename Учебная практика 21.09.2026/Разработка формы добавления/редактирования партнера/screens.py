from html import escape

from navigation import EDIT, LIST, MISSING, PARTNER
from partner_edit import PartnerEditWindow


def shell(title, trail, body, actions=""):
    crumbs = " → ".join(escape(item) for item in trail)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="icon" href="/resources/app_icon.png" type="image/png">
  <link rel="stylesheet" href="/static/style.css">
  <link rel="stylesheet" href="/static/form.css">
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


def render_list(partners, selected_partner_id, trail):
    cards = []
    for partner in partners:
        selected = " selected" if partner["partner_id"] == selected_partner_id else ""
        title = f"{partner['partner_type']} | {partner['company_name']}"
        cards.append(
            f"""
            <a class="card card-link{selected}" href="/partner/{partner['partner_id']}">
              <div>
                <h2>{escape(title)}</h2>
                <p>{escape(str(partner.get('director') or '—'))}</p>
                <p>{escape(str(partner.get('phone') or '—'))}</p>
                <p>Рейтинг: {escape(str(partner.get('rating') or '—'))}</p>
              </div>
              <div class="discount">{format_discount(partner.get('discount_percent'))}</div>
            </a>
            """
        )
    body = f'<section class="board" aria-label="Список партнеров">{"".join(cards)}</section>'
    actions = (
        '<a class="btn" href="/partner/new">Добавить партнера</a>'
        '<a class="btn" href="/">Обновить список</a>'
    )
    return shell("CRM: Список партнеров и скидок", trail, body, actions)


def render_partner(partner, trail):
    title = f"{partner['partner_type']} | {partner['company_name']}"
    body = f"""
    <section class="board">
      <article class="card">
        <div>
          <h2>{escape(title)}</h2>
          <p>Директор: {escape(str(partner.get('director') or '—'))}</p>
          <p>Email: {escape(str(partner.get('contact_email') or '—'))}</p>
          <p>Телефон: {escape(str(partner.get('phone') or '—'))}</p>
          <p>Рейтинг: {escape(str(partner.get('rating') or '—'))}</p>
        </div>
        <div class="discount">{format_discount(partner.get('discount_percent'))}</div>
      </article>
    </section>
    """
    partner_id = partner["partner_id"]
    actions = (
        f'<a class="btn" href="/back">Назад</a>'
        f'<a class="btn" href="/partner/{partner_id}/edit">Редактировать</a>'
    )
    return shell("CRM: Карточка партнера", trail, body, actions)


def render_edit(window: PartnerEditWindow, trail):
    body = f'<section class="board">{window.render_form()}</section>'
    return shell(window.title(), trail, body)


def render_missing(partner_id, trail):
    body = (
        '<section class="board">'
        f"<p class='empty'>Партнер № {escape(str(partner_id))} не найден. "
        "Приложение продолжает работу.</p>"
        "</section>"
    )
    actions = '<a class="btn" href="/back">Назад</a>'
    return shell("CRM: Партнер не найден", trail, body, actions)


def render_screen(screen, params, *, partners=None, partner=None, window=None, selected_partner_id=None, trail=None):
    trail = trail or []
    if screen == LIST:
        return render_list(partners or [], selected_partner_id, trail)
    if screen == PARTNER:
        return render_partner(partner, trail)
    if screen == EDIT:
        return render_edit(window, trail)
    if screen == MISSING:
        return render_missing(params.get("partner_id"), trail)
    return render_list(partners or [], selected_partner_id, trail)
