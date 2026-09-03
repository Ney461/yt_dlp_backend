import tkinter as tk

from components.url_input import UrlInput
from components.title import Title
from components.section import Section
from components.video_info import VideoInfo
from components.download_options import DownloadOptions
from utils.colors import MAIN_BG

class MainView(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent, background=MAIN_BG)
        
        self.header = Title(self)
        self.header.pack(fill='x')
            
        self.url_input = UrlInput(self)
        self.url_input.pack()
        
        self.video_section_container = Section(self, "Información del video")
        self.video_section_container.pack(pady=10)
        
        self.video_info = VideoInfo(self.video_section_container)
        self.video_info.pack(anchor="nw", fill="x")
        
        self.download_section_container = Section(self, "Opciones de descargas")
        self.download_section_container.pack(pady=20)
        
        self.download_options = DownloadOptions(self.download_section_container)
        self.download_options.pack(anchor="nw", fill="x")