import subprocess
import threading
import time
import sys
from pathlib import Path

import tkinter as tk

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"

backendProcess = subprocess.Popen(
    [str(VENV_PYTHON), "-m", "uvicorn", "ytdlp_api.main:app", "--port", "8000"],
    cwd=PROJECT_ROOT / "src",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    creationflags=subprocess.CREATE_NO_WINDOW
)


def log_backend_output():
    for line in backendProcess.stdout:
        print(f"[BACKEND] {line}", end="", flush=True)


logThread = threading.Thread(target=log_backend_output, daemon=True)
logThread.start()

time.sleep(3)


def stopBackend():
    backendProcess.terminate()
    try:
        backendProcess.wait(timeout=5)
    except subprocess.TimeoutExpired:
        backendProcess.kill()


try:
    from views.main_view import MainView

    def onClose():
        stopBackend()
        root.destroy()

    root = tk.Tk()
    root.title("Descargar gratis")
    root.geometry("800x600")

    root.protocol("WM_DELETE_WINDOW", onClose)

    app = MainView(root)
    app.pack(fill="both", expand=True)

    root.mainloop()

except Exception as error:
    print(f"Error al iniciar la aplicacion: {error}")

finally:
    stopBackend()