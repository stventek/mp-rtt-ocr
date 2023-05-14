import customtkinter
from data import getBoundData
from logger import CallBackLogger
from translate_word import deepl_lang_codes, google_lang_codes
import tkinter as tk
import logging

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MainTK():

    def __init__(self):
        self.data = getBoundData()
        self.app = customtkinter.CTk()
        self.app.title("Real time  OCR translate")
        self.width = 1200
        self.height = 900
        self.app.geometry(f'{self.width // 2}x{self.height}+{800}+{0}')

        self.logger = CallBackLogger('MainTK', self.add_log, logging.DEBUG)

        self.frame_1 = customtkinter.CTkFrame(master=self.app)
        self.frame_1.pack(pady=20, padx=60, fill="both", expand=True)

        self.translation_count = 0
        self.translation_timeouts = 0

        self.button_select_frame = customtkinter.CTkButton(master=self.frame_1, 
            text="Select frame", 
            command=self.select_frame, 
            font=("Arial", 16), 
            border_spacing=8)
        self.button_select_frame.pack(pady=(20,5), padx=10)

        self.label_1_translator = customtkinter.CTkLabel(master=self.frame_1, text="Translator", font=("Arial", 16))
        self.label_1_translator.pack(pady=5, padx=10)

        self.combobox_translator = customtkinter.CTkComboBox(self.frame_1, 
            state="readonly", 
            values=["Deepl", "Google"],
            command=self.update_from_to_comboboxes)
        
        self.combobox_translator.pack(pady=5, padx=10)
        self.combobox_translator.set("Deepl")

        self.label_2 = customtkinter.CTkLabel(master=self.frame_1, text="From", font=("Arial", 16))
        self.label_2.pack(pady=5, padx=10)

        self.combobox_from = customtkinter.CTkComboBox(self.frame_1, state="readonly", values=list(deepl_lang_codes.keys()))
        self.combobox_from.pack(pady=5, padx=10)
        self.combobox_from.set("English")

        self.label_3 = customtkinter.CTkLabel(master=self.frame_1, text="To", font=("Arial", 16))
        self.label_3.pack(pady=5, padx=10)

        self.combobox_to = customtkinter.CTkComboBox(self.frame_1, state="readonly", values=list(deepl_lang_codes.keys()))
        self.combobox_to.pack(pady=(5), padx=10)
        self.combobox_to.set("Spanish")

        self.button_advance_settings = customtkinter.CTkButton(master=self.frame_1, text="Advanced settigns", command=self.select_frame, font=("Arial", 16), border_spacing=8)
        self.button_advance_settings.pack(pady=(15), padx=10)

        self.frame_metadata = customtkinter.CTkFrame(master=self.app)
        self.frame_metadata.pack(pady=(0,20), padx=60, fill="both", expand=True)

        self.label_metadata = customtkinter.CTkLabel(master=self.frame_metadata, text="Metadata", font=("Arial", 24))
        self.label_metadata.pack(pady=(20,5), padx=10)

        self.label_translation_count = customtkinter.CTkLabel(master=self.frame_metadata, text="Translation count: 0", font=("Arial", 16))
        self.label_translation_count.pack(pady=5, padx=10)

        self.label_translation_timeouts = customtkinter.CTkLabel(master=self.frame_metadata, text="Translation timeouts: 0", font=("Arial", 16))
        self.label_translation_timeouts.pack(pady=5, padx=10)

        self.frame_logs = customtkinter.CTkFrame(master=self.app)
        self.frame_logs.pack(pady=(0,20), padx=60, fill="both", expand=True)

        self.label_logs = customtkinter.CTkLabel(master=self.frame_logs, text="Logs", font=("Arial", 24))
        self.label_logs.pack(pady=(20,5), padx=10)

        self.textbox_logs = customtkinter.CTkTextbox(master=self.frame_logs)
        self.textbox_logs.pack(pady=15, padx=20,  fill="both", expand=True)

    def add_log(self, log):
        self.textbox_logs.configure(state="normal") 
        self.textbox_logs.insert(tk.END, log + "\n")
        self.textbox_logs.see(tk.END)
        self.textbox_logs.configure(state="disabled") 
        self.textbox_logs.update()

    def add_translation_count(self):
        self.translation_count += 1
        self.label_translation_count.configure(text=f"Translation count: {self.translation_count}")

    def add_translation_timeout(self):
        self.translation_timeouts += 1
        self.label_translation_timeouts.configure(text=f"Translation timeouts: {self.translation_timeouts}")

    def update_from_to_comboboxes(self, choice):
        if choice == "Deepl":
            self.combobox_from.configure(values=list(deepl_lang_codes.keys()))
            self.combobox_to.configure(values=list(deepl_lang_codes.keys()))
        elif choice == "Google":
            self.combobox_from.configure(values=list(google_lang_codes.keys()))
            self.combobox_to.configure(values=list(google_lang_codes.keys()))

    def minimize_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.iconify()

    def bring_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.deiconify()

    def minimize_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.iconify()

    def select_frame(self):
        self.minimize_child_windows()
        self.app.iconify()
        import selectable_frame
        selectable_frame.SelectableFrame(self)