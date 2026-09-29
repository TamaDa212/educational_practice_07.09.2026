from html import escape

from order_calculator import list_material_types, list_product_types


def render_calculator(values, result=None):
    product_lines = []
    for item in list_product_types():
        product_lines.append(
            f"<li>{item['product_type_id']} — {escape(item['type_name'])}, коэффициент {item['coefficient']}</li>"
        )
    material_lines = []
    for item in list_material_types():
        material_lines.append(
            f"<li>{item['material_type_id']} — {escape(item['type_name'])}, брак {item['defect_percent']}%</li>"
        )
    if result is None:
        result_block = ""
    elif result["ok"]:
        result_block = f'<p class="result ok">{escape(result["message"])}</p>'
    else:
        result_block = f'<p class="result error" role="alert">{escape(result["message"])}</p>'
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CRM: Калькулятор заказа</title>
  <link rel="icon" href="/resources/app_icon.png" type="image/png">
  <link rel="stylesheet" href="/static/style.css">
  <link rel="stylesheet" href="/static/calculator.css">
</head>
<body>
  <main class="window">
    <div class="window-bar">
      <img src="/resources/app_icon.png" alt="Иконка приложения">
      <span>CRM: Калькулятор заказа</span>
    </div>
    <header class="header">
      <img src="/resources/company_logo.png" alt="Логотип компании Альянс">
      <h1>CRM: Калькулятор заказа</h1>
    </header>
    <section class="board">
      <form class="order-form" method="post" action="/calculate">
        <label>
          ID типа продукции
          <input type="text" name="product_type_id" value="{escape(values['product_type_id'])}">
        </label>
        <label>
          ID типа материала
          <input type="text" name="material_type_id" value="{escape(values['material_type_id'])}">
        </label>
        <label>
          Количество продукции
          <input type="text" name="quantity" value="{escape(values['quantity'])}">
        </label>
        <label>
          Размер продукции, параметр 1
          <input type="text" name="param_1" value="{escape(values['param_1'])}">
        </label>
        <label>
          Размер продукции, параметр 2
          <input type="text" name="param_2" value="{escape(values['param_2'])}">
        </label>
        <button type="submit">Рассчитать</button>
      </form>
      {result_block}
      <div class="hints">
        <p>Типы продукции</p>
        <ul>{"".join(product_lines)}</ul>
        <p>Типы материалов</p>
        <ul>{"".join(material_lines)}</ul>
      </div>
    </section>
  </main>
</body>
</html>
"""
