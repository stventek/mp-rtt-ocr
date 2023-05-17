import tkinter.ttk as ttk
import customtkinter as ck

theme = ck.ThemeManager()

class CustomLabelFrame(ttk.LabelFrame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.frame_group = ck.CTkFrame(master=self)
        self.frame_group.pack(fill="both", expand=True)
