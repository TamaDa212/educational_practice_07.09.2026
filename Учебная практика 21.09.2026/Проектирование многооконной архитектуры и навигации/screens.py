from html import escape

from navigation import HISTORY, LIST, MISSING, PARTNER


def shell(title, trail, body, actions):
    crumbs = " → ".join(escape(item) for item in trail)
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="icon" href="/resources/app_icon.png" type="image/png">
  <link rel="stylesheet" href="/static/style.css">
  <link rel="stylesheet" href="/static/nav.css">
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
    <div class="actions">
      {actions}
    </div>
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
    actions = '<a class="btn" href="/">Обновить список</a>'
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
          <p>Объём закупок: {escape(str(partner.get('total_quantity') or 0))}</p>
        </div>
        <div class="discount">{format_discount(partner.get('discount_percent'))}</div>
      </article>
    </section>
    """
    partner_id = partner["partner_id"]
    actions = (
        f'<a class="btn" href="/back">Назад</a>'
        f'<a class="btn" href="/partner/{partner_id}/history">История продаж</a>'
    )
    return shell("CRM: Карточка партнера", trail, body, actions)


def render_history(partner, sales, trail):
    if sales:
        rows = []
        for item in sales:
            rows.append(
                "<tr>"
                f"<td>{escape(str(item['sale_date']))}</td>"
                f"<td>{escape(str(item['product_name']))}</td>"
                f"<td>{item['quantity']}</td>"
                f"<td>{item['total_amount']:.2f}</td>"
                "</tr>"
            )
        table = (
            "<table class='sales'><thead><tr>"
            "<th>Дата</th><th>Товар</th><th>Кол-во</th><th>Сумма</th>"
            "</tr></thead><tbody>"
            + "".join(rows)
            + "</tbody></table>"
        )
    else:
        table = "<p class='empty'>Истории продаж нет. Скидка 0%.</p>"
    title = f"{partner['partner_type']} | {partner['company_name']}"
    body = f'<section class="board"><h2>{escape(title)}</h2>{table}</section>'
    actions = '<a class="btn" href="/back">Назад</a><a class="btn" href="/">К списку</a>'
    return shell("CRM: История продаж", trail, body, actions)


def render_missing(partner_id, trail):
    body = (
        '<section class="board">'
        f"<p class='empty'>Партнер № {escape(str(partner_id))} не найден. "
        "Приложение продолжает работу.</p>"
        "</section>"
    )
    actions = '<a class="btn" href="/back">Назад</a>'
    return shell("CRM: Партнер не найден", trail, body, actions)


def render_screen(screen, params, *, partners=None, partner=None, sales=None, selected_partner_id=None, trail=None):
    trail = trail or []
    if screen == LIST:
        return render_list(partners or [], selected_partner_id, trail)
    if screen == PARTNER:
        return render_partner(partner, trail)
    if screen == HISTORY:
        return render_history(partner, sales or [], trail)
    if screen == MISSING:
        return render_missing(params.get("partner_id"), trail)
    return render_list(partners or [], selected_partner_id, trail)
