import tkinter as tk

from utils.styles import LABEL_STYLE
from utils.colors import MAIN_BG

class VideoInfo(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=MAIN_BG
        )

        self.title_label = tk.Label(
            self,
            text="Título:",
            **LABEL_STYLE
        )
        self.title_label.pack(anchor="w")
        

        self.duration_label = tk.Label(
            self,
            text="Duración:",
            **LABEL_STYLE
        )
        self.duration_label.pack(anchor="w")
        