import tkinter as tk

from utils.colors import BUTTON_ACT_BG, BUTTON_BG
from utils.styles import BUTTON_STYLE


class StyledButton(tk.Button):

    def __init__(self, parent, text: str, command=None):
        super().__init__(
            parent,
            text=text,
            command=command,
            **BUTTON_STYLE,
            padx=6,
            pady=6
        )

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.config(bg=BUTTON_ACT_BG)

    def _on_leave(self, event):
        self.config(bg=BUTTON_BG)