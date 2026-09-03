import tkinter as tk
from tkinter import ttk

from utils.COLORS import *
from utils.STYLES import LABEL_STYLE
from .button import ButtonC


class UrlInput(tk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=MAIN_BG,
            padx=5,
            pady=20
        )

        self.label = tk.Label(
            self,
            text="URL",
            **LABEL_STYLE
        )
        self.label.grid(
            row=0,
            column=0,
            padx=(0, 8)
        )

        self.style = ttk.Style()
        self.style.configure(
            "MarginEntry.TEntry",
            padding=8
        )

        self.entry = ttk.Entry(
            self,
            width=60,
            style="MarginEntry.TEntry"
        )
        self.entry.grid(
            row=0,
            column=1,
            padx=(0, 8),
            pady=10
        )

        self.button = ButtonC(
            self,
            "Obtener Información"
        )
        self.button.grid(
            row=0,
            column=2,
            padx=(0, 5)
        )