import tkinter as tk
from views.main_view import MainView

root = tk.Tk()
root.title("Descargar gratis")
root.geometry("700x500")


app = MainView(root)
app.pack(fill="both", expand=True)

root.mainloop()