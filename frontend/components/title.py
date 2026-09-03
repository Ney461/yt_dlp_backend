import tkinter as tk
from utils.COLORS import *
from utils.STYLES import TITLE_STYLE


class Title(tk.Frame):

    def __init__(self, parent):
        super().__init__(
            parent,
            bg=HEADER_BG,
            height=65
        )

        self.pack_propagate(False)

        self.title = tk.Label(
            self,
            text="App para descargar música y videos",
            **TITLE_STYLE
        )

        self.title.pack(
            expand=True
        )