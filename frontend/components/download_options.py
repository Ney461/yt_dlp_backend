import tkinter as tk

from utils.STYLES import LABEL_STYLE, CHECKBUTTON_STYLE
from utils.COLORS import MAIN_BG
from components.styled_select import StyledSelect
from utils.OPTIONS_DOWNLOAD import *

class DownloadOptions(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=MAIN_BG
        )


        self.type = tk.Label(
            self,
            text="Tipo:",
            **LABEL_STYLE
        )
        self.type.grid(row=0, column=0, sticky="w")
        
        self.typeSelector = StyledSelect(
            self,
            values=["Video", "Audio"],
            default=["Video"]
        )
        self.typeSelector.grid(row=0, column=1, sticky="w")
        

        self.format = tk.Label(
            self,
            text="Formato:",
            **LABEL_STYLE
        )
        self.format.grid(row=1, column=0, sticky="w")
        
        self.formatSelector = StyledSelect(
            self,
            values= VIDEO_FORMATS,
            default=[VIDEO_FORMATS[0]]
        )
        self.formatSelector.grid(row=1, column=1, sticky="w")

        self.quality = tk.Label(
            self,
            text="Calidad:",
            **LABEL_STYLE
        )
        self.quality.grid(row=2, column=0, sticky="w")

        self.qualitySelector = StyledSelect(
            self,
            values= VIDEO_QUALITY_FORMATS,
            default=[VIDEO_QUALITY_FORMATS[-1]]
        )
        self.qualitySelector.grid(row=2, column=1, sticky="w")  

        self.lbMetadata = tk.Label(
            self,
            text="Metadata:   ",
            **LABEL_STYLE
        )
        self.lbMetadata.grid(row=3, column=0, sticky="w")
        
        self.checkMetadata = tk.Checkbutton(self, **CHECKBUTTON_STYLE)
        self.checkMetadata.grid(row=3, column=1, sticky="w")
        