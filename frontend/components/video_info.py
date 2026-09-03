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

    def update_data(self, video_data):
        title = video_data.get("title", "Desconocido")
        duration_seconds = video_data.get("duration", 0)

        self.title_label.config(text=f"Título: {title}")
        self.duration_label.config(text=f"Duración: {self._format_duration(duration_seconds)}")

    @staticmethod
    def _format_duration(seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"

        return f"{minutes}:{remaining_seconds:02d}"