import tkinter as tk

from utils.styles import LABEL_STYLE, CHECKBUTTON_STYLE
from utils.colors import MAIN_BG
from components.styled_select import StyledSelect
from utils.download_options import AUDIO_FORMATS, VIDEO_FORMATS, VIDEO_QUALITY_FORMATS

class DownloadOptions(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=MAIN_BG
        )


        self.type_label = tk.Label(
            self,
            text="Tipo:",
            **LABEL_STYLE
        )
        self.type_label.grid(row=0, column=0, sticky="w")
        
        self.type_selector = StyledSelect(
            self,
            values=["Video", "Audio"],
            default="Video",
            command=self._handle_type_change,
        )
        self.type_selector.grid(row=0, column=1, sticky="w")
        

        self.format_label = tk.Label(
            self,
            text="Formato:",
            **LABEL_STYLE
        )
        self.format_label.grid(row=1, column=0, sticky="w")
        
        self.format_selector = StyledSelect(
            self,
            values=VIDEO_FORMATS,
            default=VIDEO_FORMATS[0]
        )
        self.format_selector.grid(row=1, column=1, sticky="w")

        self.quality_label = tk.Label(
            self,
            text="Calidad:",
            **LABEL_STYLE
        )
        self.quality_label.grid(row=2, column=0, sticky="w")

        self.quality_selector = StyledSelect(
            self,
            values=VIDEO_QUALITY_FORMATS,
            default=VIDEO_QUALITY_FORMATS[-1]
        )
        self.quality_selector.grid(row=2, column=1, sticky="w")

        self.metadata_label = tk.Label(
            self,
            text="Metadata:   ",
            **LABEL_STYLE
        )
        self.metadata_label.grid(row=3, column=0, sticky="w")
        
        self.metadata_checked = tk.BooleanVar(value=False)
        self.metadata_checkbutton = tk.Checkbutton(
            self,
            variable=self.metadata_checked,
            **CHECKBUTTON_STYLE
        )
        self.metadata_checkbutton.grid(row=3, column=1, sticky="w")
        self._handle_type_change(self.type_selector.get_value())

    def _handle_type_change(self, download_type):
        is_video = download_type == "Video"
        self._update_format_options(is_video)
        self._set_quality_visibility(is_video)

    def _update_format_options(self, is_video):
        formats = VIDEO_FORMATS if is_video else AUDIO_FORMATS
        self.format_selector.set_values(formats, formats[0])

    def _set_quality_visibility(self, is_visible):
        if is_visible:
            self.quality_label.grid()
            self.quality_selector.grid()
        else:
            self.quality_label.grid_remove()
            self.quality_selector.grid_remove()

    def get_options(self):
        return {
            "type": self.type_selector.get_value(),
            "format": self.format_selector.get_value(),
            "quality": self.quality_selector.get_value() if self._is_video() else None,
            "metadata": self.metadata_checked.get(),
        }

    def _is_video(self):
        return self.type_selector.get_value() == "Video"
        