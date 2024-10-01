from tkinter import *
from customtkinter import *
from bloch_frame import render_bloch_frame
from settings_bar_frame import render_settings_bar_frame
from state import State
from gate import Gate

root = CTk()

render_bloch_frame(root)
render_settings_bar_frame(root, lambda: render_bloch_frame(root))


def center_window(window):
    window.update_idletasks()
    width, height = window.winfo_reqwidth(), window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


center_window(root)

root.wm_title("Bloch sphere simulator")


root.mainloop()
