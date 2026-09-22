LIST = "list"
PARTNER = "partner"
HISTORY = "history"
MISSING = "missing"


def parse_partner_id(value):
    if value is None:
        return None
    try:
        partner_id = int(value)
    except (TypeError, ValueError):
        return None
    if partner_id <= 0:
        return None
    return partner_id


class Navigator:
    """Стек экранов: список → карточка → история. Назад не закрывает приложение."""

    def __init__(self):
        self.selected_partner_id = None
        self.stack = [(LIST, {})]

    @property
    def current(self):
        return self.stack[-1]

    @property
    def screen(self):
        return self.current[0]

    @property
    def params(self):
        return self.current[1]

    def open_list(self):
        self.stack = [(LIST, {})]
        return self.current

    def open_partner(self, partner_id):
        parsed = parse_partner_id(partner_id)
        if parsed is None:
            self.stack = [(LIST, {}), (MISSING, {"partner_id": partner_id})]
            return self.current
        self.selected_partner_id = parsed
        self.stack = [(LIST, {}), (PARTNER, {"partner_id": parsed})]
        return self.current

    def open_history(self, partner_id):
        parsed = parse_partner_id(partner_id)
        if parsed is None:
            self.stack = [(LIST, {}), (MISSING, {"partner_id": partner_id})]
            return self.current
        self.selected_partner_id = parsed
        self.stack = [
            (LIST, {}),
            (PARTNER, {"partner_id": parsed}),
            (HISTORY, {"partner_id": parsed}),
        ]
        return self.current

    def back(self):
        if len(self.stack) > 1:
            self.stack.pop()
        return self.current

    def trail(self):
        names = {
            LIST: "Список партнеров",
            PARTNER: "Карточка партнера",
            HISTORY: "История продаж",
            MISSING: "Партнер не найден",
        }
        return [names[item[0]] for item in self.stack]
