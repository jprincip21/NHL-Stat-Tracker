from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap import Querybox

root = tb.Window(themename="darkly")

root.title("GUI Testing, Date Entry")
root.iconbitmap('assets/logo.ico')
root.geometry('500x350')

enter_date = tb.DateEntry(root, bootstyle="darkly")
enter_date.pack(pady=50)

root.mainloop()