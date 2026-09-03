import tkinter as tk
from utils.COLORS import MAIN_BG, ACCENT_COLOR
from utils.FONTS import FONT_LABEL


class Section(tk.LabelFrame):

    def __init__(self, parent, title: str):
        super().__init__(
            parent,
            text=f"    {title}    ",
            bg=MAIN_BG,
            fg=ACCENT_COLOR,
            font=FONT_LABEL,
            padx=10,
            pady=10,
        )