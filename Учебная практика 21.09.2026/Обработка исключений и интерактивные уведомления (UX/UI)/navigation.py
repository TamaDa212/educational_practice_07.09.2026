LIST = "list"
EDIT = "edit"
MISSING = "missing"


def parse_partner_id(value):
    if value is None or value == "":
        return None
    try:
        partner_id = int(value)
    except (TypeError, ValueError):
        return None
    if partner_id <= 0:
        return None
    return partner_id


class Navigator:
    def __init__(self):
        self.selected_partner_id = None
        self.dialog = None
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

    def open_list(self, dialog=None):
        self.stack = [(LIST, {})]
        self.dialog = dialog
        return self.current

    def open_edit(self, partner_id=None):
        parsed = parse_partner_id(partner_id)
        if partner_id not in (None, "", "new") and parsed is None:
            self.stack = [(LIST, {}), (MISSING, {"partner_id": partner_id})]
            return self.current
        self.dialog = None
        if parsed is not None:
            self.selected_partner_id = parsed
            self.stack = [(LIST, {}), (EDIT, {"partner_id": parsed})]
        else:
            self.stack = [(LIST, {}), (EDIT, {"partner_id": None})]
        return self.current

    def back(self):
        if len(self.stack) > 1:
            self.stack.pop()
        return self.current

    def trail(self):
        names = {
            LIST: "Список партнеров",
            EDIT: "PartnerEditWindow",
            MISSING: "Партнер не найден",
        }
        return [names[item[0]] for item in self.stack]
