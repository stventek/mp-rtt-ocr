import customtkinter as ck
from windows.main_window.frames.form_frame import FormFrame
from windows.main_window.frames.custom_label_frame import CustomLabelFrame
from customtkinter import ThemeManager
import tkinter as tk
from main_window_wrapper import MainTKWrapper

class MainTKFrame(ck.CTkFrame):
    def __init__(self, mainW: MainTKWrapper, *args, **kwargs):
        ck.CTkFrame.__init__(self, *args, **kwargs)
        self.mainW = mainW

        self.group_label_logs = CustomLabelFrame(self,
            text="Logs", 
        )

        self.label_logs = ck.CTkLabel(master=self.group_label_logs.frame_group, text="Logs", font=("Arial", 24))
        self.label_logs.pack(pady=(20,5), padx=10)

        self.textbox_logs = ck.CTkTextbox(master=self.group_label_logs.frame_group, state='disabled')
        self.textbox_logs.pack(pady=15, padx=20,  fill="both", expand=True)

        self.controls_frame = FormFrame(mainW, master=self, fg_color=ThemeManager.theme['CTk']['fg_color'])
        self.controls_frame.pack(fill='y', side='right', padx=(0,10), pady=10)
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_rowconfigure(0, weight=1)
        self.controls_frame.grid_rowconfigure(1, weight=1)

    def add_log(self, log):
        self.textbox_logs.configure(state="normal") 
        self.textbox_logs.insert(tk.END, log + "\n")
        self.textbox_logs.see(tk.END)
        self.textbox_logs.configure(state="disabled") 
        self.textbox_logs.update()