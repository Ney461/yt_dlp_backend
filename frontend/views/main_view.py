import os, time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import re
from urllib.parse import unquote
import requests

from components.url_input import UrlInput
from components.title import Title
from components.section import Section
from components.video_info import VideoInfo
from components.download_options import DownloadOptions
from components.styled_button import StyledButton
from utils.colors import ACCENT_COLOR, HEADER_BG, MAIN_BG, WHITE
from utils.fonts import FONT_LABEL
from services.api_client import *


class MainView(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, background=MAIN_BG)

        self.header = Title(self)
        self.header.pack(fill='x')

        self.url_input = UrlInput(self, on_submit=self.on_video_found)
        self.url_input.pack()

        self.video_section_container = Section(self, "Información del video")

        self.video_info = VideoInfo(self.video_section_container)
        self.video_info.pack(anchor="nw", fill="x")

        self.download_section_container = Section(self, "Opciones de descargas")

        self.download_options = DownloadOptions(self.download_section_container)
        self.download_options.pack(anchor="nw", fill="x")

        self.download_button = StyledButton(self, "Descargar", command=self.on_download_click)
        
        self._configure_progress_style()
        self.progress_bar = ttk.Progressbar(
            self,
            mode="determinate",
            length=300,
            style="Download.Horizontal.TProgressbar",
        )
        self.status_label = tk.Label(
            self,
            text="",
            bg=MAIN_BG,
            fg=WHITE,
            font=FONT_LABEL,
        )

    def _configure_progress_style(self):
        progress_style = ttk.Style()
        progress_style.configure(
            "Download.Horizontal.TProgressbar",
            troughcolor=HEADER_BG,
            background=ACCENT_COLOR,
            bordercolor=HEADER_BG,
            lightcolor=ACCENT_COLOR,
            darkcolor=ACCENT_COLOR,
            thickness=14,
        )

    def show_results(self):
        self._set_results_visibility(True)

    def hide_results(self):
        self._set_results_visibility(False)

    def _set_results_visibility(self, is_visible):
        if is_visible:
            self.video_section_container.pack(pady=10)
            self.download_section_container.pack(pady=20)
            self.download_button.pack()
            return

        self.video_section_container.pack_forget()
        self.download_section_container.pack_forget()
        self.download_button.pack_forget()

    def on_video_found(self, video_data):
        self.video_info.update_data(video_data)
        self.download_options.update_qualities(video_data.get("max_height"))
        self.show_results()

    # def on_download_click(self):
    #     url = self.url_input.get_url()

    #     if not url:
    #         messagebox.showwarning("URL vacia", "Primero ingresa una URL valida.")
    #         return

    #     request_payload = {
    #         "url": url,
    #         **self.download_options.get_options()
    #     }

    #     self.download_button.config(state="disabled", text="Descargando...")

    #     thread = threading.Thread(
    #         target=self._download_worker,
    #         args=(request_payload,),
    #         daemon=True
    #     )
    #     thread.start()

    # def _download_worker(self, request_payload):
    #     try:
    #         response = download_media(request_payload)

    #         if response.status_code != 200:
    #             self.after(0, self._on_download_error, f"No se pudo descargar el archivo (status {response.status_code}).")
    #             return

    #         self.after(0, self._on_download_success, response, request_payload["file_format"])

    #     except Exception as error:
    #         self.after(0, self._on_download_error, str(error))

    # def _on_download_success(self, response, fallback_ext):
    #     filename = self._extract_filename(response, fallback_ext)

    #     save_path = filedialog.asksaveasfilename(
    #         initialfile=filename,
    #         defaultextension=os.path.splitext(filename)[1]
    #     )

    #     if not save_path:
    #         self._reset_ui()
    #         return

    #     threading.Thread(
    #         target=self._save_worker,
    #         args=(response.content, save_path),
    #         daemon=True
    #     ).start()

    # def _save_worker(self, content, save_path):
    #     try:
    #         with open(save_path, "wb") as file:
    #             file.write(content)
    #     except OSError as error:
    #         self.after(0, self._on_download_error, str(error))
    #         return

    #     self.after(0, self._on_download_finished_ok)

    # def _on_download_finished_ok(self):
    #     messagebox.showinfo("Descarga completa", "El archivo se guardo correctamente.")
    #     self._reset_ui()

    # def _on_download_error(self, message):
    #     messagebox.showerror("Error", message)
    #     self._reset_ui()

    # def _reset_ui(self):
    #     self.download_button.config(state="normal", text="Descargar")
    #     self.url_input.clear()
    #     self.hide_results()
    
    def on_download_click(self):
        url = self.url_input.get_url()

        if not url:
            messagebox.showwarning("URL vacia", "Primero ingresa una URL valida.")
            return

        request_payload = {
            "url": url,
            **self.download_options.get_options()
        }

        self.download_button.config(state="disabled", text="Descargando...")
        self.progress_bar.pack(fill="x", padx=20, pady=(10, 4))
        self.status_label.pack(pady=(0, 6))
        self.progress_bar["value"] = 0

        thread = threading.Thread(
            target=self._start_job_worker,
            args=(request_payload,),
            daemon=True
        )
        thread.start()

    def _start_job_worker(self, request_payload):
        try:
            response = start_download(request_payload)

            if response.status_code != 200:
                self.after(0, self._on_download_error, "No se pudo iniciar la descarga.")
                return

            job_id = response.json()["job_id"]
            self._poll_progress(job_id, request_payload["file_format"])

        except Exception as error:
            self.after(0, self._on_download_error, str(error))

    def _poll_progress(self, job_id, fallback_ext):
        while True:
            time.sleep(0.5)

            try:
                response = get_download_progress(job_id)
            except Exception as error:
                self.after(0, self._on_download_error, str(error))
                return

            if response.status_code != 200:
                self.after(0, self._on_download_error, "Error consultando el progreso.")
                return

            job = response.json()
            status = job.get("status")

            if status == "downloading":
                self.after(0, self._update_progress, job.get("percent", 0), "Descargando...")

            elif status == "processing":
                self.after(0, self._update_progress, 100, "Procesando archivo...")

            elif status == "finished":
                self.after(0, self._fetch_file, job_id, fallback_ext)
                return

            elif status == "error":
                self.after(0, self._on_download_error, job.get("error", "Error desconocido."))
                return

    def _update_progress(self, percent, status_text):
        self.progress_bar["value"] = percent
        self.status_label.config(text=f"{status_text} {percent}%")

    def _fetch_file(self, job_id, fallback_ext):
        self.status_label.config(text="Descargando archivo final...")

        thread = threading.Thread(
            target=self._download_file_worker,
            args=(job_id, fallback_ext),
            daemon=True
        )
        thread.start()

    def _download_file_worker(self, job_id, fallback_ext):
        try:
            response = get_download_file(job_id)
        except Exception as error:
            self.after(0, self._on_download_error, str(error))
            return

        if response.status_code != 200:
            self.after(0, self._on_download_error, "No se pudo obtener el archivo.")
            return

        self.after(0, self._on_download_success, response, fallback_ext)

    def _on_download_success(self, response, fallback_ext):
        filename = self._extract_filename(response, fallback_ext)

        save_path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=os.path.splitext(filename)[1]
        )

        if not save_path:
            self._reset_ui()
            return

        threading.Thread(
            target=self._save_worker,
            args=(response.content, save_path),
            daemon=True
        ).start()

    def _save_worker(self, content, save_path):
        try:
            with open(save_path, "wb") as file:
                file.write(content)
        except OSError as error:
            self.after(0, self._on_download_error, str(error))
            return

        self.after(0, self._on_download_finished_ok)

    def _on_download_finished_ok(self):
        messagebox.showinfo("Descarga completa", "El archivo se guardo correctamente.")
        self._reset_ui()

    def _on_download_error(self, message):
        messagebox.showerror("Error", message)
        self._reset_ui()

    def _reset_ui(self):
        self.download_button.config(state="normal", text="Descargar")
        self.progress_bar.pack_forget()
        self.status_label.pack_forget()
        self.url_input.clear()
        self.hide_results()
        
    @staticmethod
    def _extract_filename(response, fallback_ext):
        content_disposition = response.headers.get("content-disposition", "")

        match = re.search(r"filename\*=utf-8''([^;]+)", content_disposition, re.IGNORECASE)

        if match:
            return unquote(match.group(1))

        match = re.search(r'filename="?([^";]+)"?', content_disposition, re.IGNORECASE)

        if match:
            return unquote(match.group(1))

        return f"descarga.{fallback_ext}" if fallback_ext else "descarga"