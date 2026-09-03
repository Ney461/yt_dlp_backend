from tkinter import ttk

from utils.colors import ACCENT_COLOR, BUTTON_ACT_BG, BUTTON_BG, HEADER_BG, MAIN_BG, WHITE
from utils.fonts import FONT_BUTTON, FONT_LABEL, FONT_TITLE


LABEL_STYLE = {
    "bg": MAIN_BG,
    "fg": WHITE,
    "font": FONT_LABEL
}


TITLE_STYLE = {
    "bg": HEADER_BG,
    "fg": ACCENT_COLOR,
    "font": FONT_TITLE
}


BUTTON_STYLE = {
    "bg": BUTTON_BG,
    "fg": WHITE,
    "activebackground": BUTTON_ACT_BG,
    "activeforeground": WHITE,
    "font": FONT_BUTTON,
    "relief": "flat",
    "bd": 0,
    "cursor": "hand2"
}

CHECKBUTTON_STYLE = {
    "bg": MAIN_BG,
    "fg": WHITE,
    "font": FONT_LABEL,
    "activebackground": MAIN_BG,
    "activeforeground": ACCENT_COLOR,
    "selectcolor": HEADER_BG,
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 0,
    "cursor": "hand2"
}


def setup_combobox_style():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "Custom.TCombobox",
        fieldbackground=HEADER_BG,
        background=HEADER_BG,
        foreground=WHITE,
        arrowcolor=ACCENT_COLOR,
        bordercolor=HEADER_BG,
        lightcolor=HEADER_BG,
        darkcolor=HEADER_BG,
        selectbackground=HEADER_BG,
        selectforeground=WHITE,
        padding=6,
        relief="flat",
        font=FONT_LABEL
    )

    style.map(
        "Custom.TCombobox",
        fieldbackground=[("readonly", HEADER_BG), ("focus", HEADER_BG), ("!focus", HEADER_BG)],
        foreground=[("readonly", WHITE), ("disabled", WHITE), ("focus", WHITE), ("!focus", WHITE)],
        bordercolor=[("focus", ACCENT_COLOR)],
        arrowcolor=[("active", ACCENT_COLOR)]
    )

    style.configure(
        "ComboboxPopdownFrame",
        background=HEADER_BG,
        bordercolor=HEADER_BG,
        relief="flat",
        borderwidth=0
    )

    style.configure(
        "Custom.Vertical.TScrollbar",
        background=HEADER_BG,
        troughcolor=HEADER_BG,
        bordercolor=HEADER_BG,
    )