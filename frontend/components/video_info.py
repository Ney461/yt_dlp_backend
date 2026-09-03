import tkinter as tk

from utils.STYLES import LABEL_STYLE
from utils.COLORS import MAIN_BG

class VideoInfo(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=MAIN_BG
        )

        self.lbTitle = tk.Label(
            self,
            text="Título:",
            **LABEL_STYLE
        )
        self.lbTitle.pack(anchor="w")
        

        self.lbTitleInput = tk.Label(
            self,
            text="Duración:",
            **LABEL_STYLE
        )
        self.lbTitleInput.pack(anchor="w")
        