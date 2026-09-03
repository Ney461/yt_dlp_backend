import tkinter as tk

from utils.COLORS import *
from utils.FONTS import FONT_BUTTON


class ButtonC(tk.Button):

    def __init__(self, parent, textBtn: str, command=None):
        super().__init__(
            parent,
            text=textBtn,
            command=command,

            # Colores
            bg=BUTTON_BG,
            fg=WHITE,
            activebackground=BUTTON_ACT_BG,
            activeforeground=WHITE,

            # Fuente
            font=FONT_BUTTON,

            # Apariencia
            relief="flat",
            bd=0,
            cursor="hand2",

            # Espaciado interno
            padx=6,
            pady=6
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.config(bg=BUTTON_ACT_BG)

    def on_leave(self, event):
        self.config(bg=BUTTON_BG)