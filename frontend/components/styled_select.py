import tkinter as tk
from tkinter import ttk

from utils.STYLES import setup_combobox_style
from utils.COLORS import MAIN_BG, WHITE, HEADER_BG


class StyledSelect(tk.Frame):

    def __init__(self, parent, values=None, default=None, command=None):
        super().__init__(parent, bg=MAIN_BG, pady=5)

        setup_combobox_style()

        self.option_add("*TCombobox*Listbox.background", HEADER_BG)
        self.option_add("*TCombobox*Listbox.foreground", WHITE)
        self.option_add("*TCombobox*Listbox.selectBackground", MAIN_BG)
        self.option_add("*TCombobox*Listbox.selectForeground", WHITE)

        self.variable = tk.StringVar()

        self.combo = ttk.Combobox(
            self,
            textvariable=self.variable,
            values=values or [],
            state="readonly",
            style="Custom.TCombobox"
        )
        self.combo.pack(fill="x")

        self.combo.bind("<<ComboboxSelected>>", self._on_select)
        self.combo.bind("<Map>", self._style_popdown)

        if default:
            self.variable.set(default)

        self.userCommand = command

    def _on_select(self, event):
        self.combo.selection_clear()
        if self.userCommand:
            self.userCommand(self.variable.get())

    def _style_popdown(self, event=None):
        popdown = self.combo.tk.eval(f"ttk::combobox::PopdownWindow {self.combo}")

        try:
            self.combo.tk.call(
                popdown, "configure",
                "-background", HEADER_BG,
                "-borderwidth", 0,
                "-highlightthickness", 0,
                "-relief", "flat"
            )
        except tk.TclError:
            pass

        frame = popdown + ".f"
        listbox = frame + ".l"
        scrollbar = frame + ".s"

        try:
            self.combo.tk.call(frame, "configure", "-background", HEADER_BG)
        except tk.TclError:
            pass

        try:
            self.combo.tk.call(
                listbox, "configure",
                "-background", HEADER_BG,
                "-foreground", WHITE,
                "-selectbackground", MAIN_BG,
                "-selectforeground", WHITE,
                "-borderwidth", 0,
                "-highlightthickness", 0
            )
        except tk.TclError:
            self.combo.tk.call(scrollbar, "configure", "-style", "Custom.Vertical.TScrollbar")
        except tk.TclError:
            pass

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)