ERROR = "error"
WARNING = "warning"
INFORMATION = "information"

TITLES = {
    ERROR: "Ошибка",
    WARNING: "Предупреждение",
    INFORMATION: "Информация",
}

ICON_LABELS = {
    ERROR: "крестик",
    WARNING: "восклицательный знак",
    INFORMATION: "инфо-значок",
}

ICONS = {
    ERROR: """
    <svg class="mb-icon mb-icon-error" viewBox="0 0 32 32" role="img" aria-label="крестик">
      <circle cx="16" cy="16" r="15" fill="#c62828"/>
      <path d="M10 10 L22 22 M22 10 L10 22" stroke="#fff" stroke-width="3" fill="none"/>
    </svg>
    """,
    WARNING: """
    <svg class="mb-icon mb-icon-warning" viewBox="0 0 32 32" role="img" aria-label="восклицательный знак">
      <polygon points="16,2 31,28 1,28" fill="#f9a825"/>
      <rect x="14.5" y="11" width="3" height="9" fill="#111"/>
      <rect x="14.5" y="22" width="3" height="3" fill="#111"/>
    </svg>
    """,
    INFORMATION: """
    <svg class="mb-icon mb-icon-information" viewBox="0 0 32 32" role="img" aria-label="инфо-значок">
      <circle cx="16" cy="16" r="15" fill="#1565c0"/>
      <rect x="14.5" y="8" width="3" height="3" fill="#fff"/>
      <rect x="14.5" y="13" width="3" height="11" fill="#fff"/>
    </svg>
    """,
}


class MessageBox:
    def __init__(self, kind, text, title=None, buttons=None):
        if kind not in TITLES:
            raise ValueError(kind)
        self.kind = kind
        self.text = text
        self.title = title or TITLES[kind]
        self.buttons = buttons or self._default_buttons()

    def _default_buttons(self):
        if self.kind == WARNING:
            return (("yes", "Да"), ("no", "Нет"))
        return (("ok", "ОК"),)

    @classmethod
    def error(cls, text):
        return cls(ERROR, text)

    @classmethod
    def warning(cls, text):
        return cls(WARNING, text)

    @classmethod
    def information(cls, text):
        return cls(INFORMATION, text)

    def render(self, box_id="app-message-box", visible=None):
        from html import escape

        if visible is None:
            visible = self.kind != WARNING
        buttons = []
        for action, label in self.buttons:
            buttons.append(
                f'<button type="button" class="mb-btn" data-action="{escape(action)}">'
                f"{escape(label)}</button>"
            )
        hidden = "" if visible else " hidden"
        return f"""
<div class="message-box-overlay{hidden}" id="{escape(box_id)}" data-kind="{self.kind}" role="presentation">
  <div class="message-box" role="alertdialog" aria-modal="true"
       aria-labelledby="{escape(box_id)}-title" aria-describedby="{escape(box_id)}-text">
    <div class="mb-title" id="{escape(box_id)}-title">{escape(self.title)}</div>
    <div class="mb-body">
      {ICONS[self.kind]}
      <p class="mb-text" id="{escape(box_id)}-text">{escape(self.text)}</p>
    </div>
    <div class="mb-actions">
      {"".join(buttons)}
    </div>
  </div>
</div>
"""
