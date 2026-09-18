from html import escape

PAGE_TITLE = "CRM: Список партнеров и скидок"


def format_discount(value) -> str:
    if value is None:
        return "0%"
    try:
        return f"{int(value)}%"
    except (TypeError, ValueError):
        return "0%"


def render_cards(partners) -> str:
    cards = []
    for partner in partners:
        title = f"{partner['partner_type']} | {partner['company_name']}"
        cards.append(
            f"""
            <article class="card">
              <div>
                <h2>{escape(title)}</h2>
                <p>{escape(str(partner.get('director') or '—'))}</p>
                <p>{escape(str(partner.get('contact_email') or '—'))}</p>
                <p>{escape(str(partner.get('phone') or '—'))}</p>
                <p>Рейтинг: {escape(str(partner.get('rating') or '—'))}</p>
              </div>
              <div class="discount">{format_discount(partner.get('discount_percent'))}</div>
            </article>
            """
        )
    return "\n".join(cards)


def render_page(partners) -> str:
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(PAGE_TITLE)}</title>
  <link rel="icon" href="/resources/app_icon.png" type="image/png">
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <main class="window">
    <div class="window-bar">
      <img src="/resources/app_icon.png" alt="Иконка приложения">
      <span>{escape(PAGE_TITLE)}</span>
    </div>
    <header class="header">
      <img src="/resources/company_logo.png" alt="Логотип компании Альянс">
      <h1>{escape(PAGE_TITLE)}</h1>
    </header>
    <section class="board" aria-label="Список партнеров">
      {render_cards(partners)}
    </section>
    <div class="actions">
      <button type="button" onclick="location.reload()">Обновить</button>
    </div>
  </main>
</body>
</html>
"""
