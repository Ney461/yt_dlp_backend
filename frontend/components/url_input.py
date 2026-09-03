import tkinter as tk
from tkinter import ttk

import requests

from utils.colors import MAIN_BG
from utils.styles import LABEL_STYLE
from components.styled_button import StyledButton
from services.api_client import get_video_info


class UrlInput(tk.Frame):

    def __init__(self, parent, on_submit=None):
        super().__init__(
            parent,
            bg=MAIN_BG,
            padx=5,
            pady=20
        )

        self.on_submit = on_submit

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

        self.button = StyledButton(
            self,
            "Obtener Información",
            command=self.search_info,
        )
        self.button.grid(
            row=0,
            column=2,
            padx=(0, 5)
        )

    def get_url(self):
        return self.entry.get().strip()

    def search_info(self):
        try:
            response = get_video_info(self.get_url())
        except requests.exceptions.RequestException:
            return

        if response.status_code == 200:
            if self.on_submit:
                self.on_submit(response.json())
                
    def clear(self):
        self.entry.delete(0, tk.END)