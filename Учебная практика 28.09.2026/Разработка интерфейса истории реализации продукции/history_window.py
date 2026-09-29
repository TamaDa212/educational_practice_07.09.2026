from html import escape


class PartnerHistoryWindow:
    """Окно истории отгрузок. partner_id приходит с главной формы."""

    def __init__(self, partner, shipments):
        self.partner = partner
        self.shipments = shipments

    @property
    def title(self):
        name = self.partner["company_name"]
        return f"CRM: История реализации продукции — {name}"

    def render(self):
        rows = []
        for item in self.shipments:
            rows.append(
                "<tr>"
                f"<td>{escape(item['product_name'])}</td>"
                f"<td>{item['quantity']}</td>"
                f"<td>{escape(item['sale_date'])}</td>"
                "</tr>"
            )
        if rows:
            body = (
                "<table class='sales'>"
                "<thead><tr>"
                "<th>Наименование продукции</th>"
                "<th>Количество (шт.)</th>"
                "<th>Дата продажи</th>"
                "</tr></thead><tbody>"
                + "".join(rows)
                + "</tbody></table>"
            )
        else:
            body = (
                "<table class='sales'>"
                "<thead><tr>"
                "<th>Наименование продукции</th>"
                "<th>Количество (шт.)</th>"
                "<th>Дата продажи</th>"
                "</tr></thead>"
                "<tbody><tr><td colspan='3'>Отгрузок по этому партнеру нет.</td></tr></tbody>"
                "</table>"
            )
        partner_id = self.partner["partner_id"]
        return f"""
        <section class="board" data-window="PartnerHistoryWindow" data-partner-id="{partner_id}">
          {body}
        </section>
        """
