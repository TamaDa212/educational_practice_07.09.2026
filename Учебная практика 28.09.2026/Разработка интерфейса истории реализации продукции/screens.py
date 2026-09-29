from html import escape

from history_window import PartnerHistoryWindow


def shell(title, body, actions):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="icon" href="/resources/app_icon.png" type="image/png">
  <link rel="stylesheet" href="/static/style.css">
  <link rel="stylesheet" href="/static/history.css">
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
    {body}
    <div class="actions">
      {actions}
    </div>
  </main>
</body>
</html>
"""


def render_list(partners, selected_partner_id, notice=""):
    cards = []
    for partner in partners:
        selected = " selected" if partner["partner_id"] == selected_partner_id else ""
        cards.append(
            f"""
            <a class="card card-link{selected}" href="/partner/{partner['partner_id']}">
              <div>
                <h2>{escape(partner['company_name'])}</h2>
                <p>{escape(str(partner.get('phone') or '—'))}</p>
                <p>Рейтинг: {escape(str(partner.get('rating') or '—'))}</p>
              </div>
            </a>
            """
        )
    banner = f'<p class="notice">{escape(notice)}</p>' if notice else ""
    body = (
        banner
        + f'<section class="board" aria-label="Список партнеров">{"".join(cards)}</section>'
    )
    if selected_partner_id:
        history = f'<a class="btn" href="/partner/{selected_partner_id}/history">История продаж</a>'
    else:
        history = '<a class="btn" href="/history">История продаж</a>'
    actions = history + '<a class="btn" href="/">Обновить список</a>'
    return shell("CRM: Список партнеров и скидок", body, actions)


def render_history(window: PartnerHistoryWindow):
    actions = '<a class="btn" href="/">К списку</a>'
    return shell(window.title, window.render(), actions)


def render_missing(partner_id):
    body = (
        '<section class="board">'
        f"<p class='empty'>Партнер № {escape(str(partner_id))} не найден.</p>"
        "</section>"
    )
    return shell("CRM: Партнер не найден", body, '<a class="btn" href="/">К списку</a>')
