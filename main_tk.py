import asyncio
import threading
import customtkinter
from frames.logs_frame import LogsFrame
from utils.main_tk_state import StateData
from utils.translate_word import deepl_lang_codes, google_lang_codes
import tkinter as tk

customtkinter.set_default_color_theme("custom_theme.json")

class MainTKWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Real time OCR translate")
        self.width = 1200
        self.height = 900
        self.geometry(f"{self.width // 2}x{self.height}+{800}+{0}")

        self.frame_1 = customtkinter.CTkFrame(master=self)
        self.frame_1.pack(pady=20, padx=60, fill="both", expand=True)

        self.button_select_frame = customtkinter.CTkButton(master=self.frame_1, 
            text="Select frame")
        self.button_select_frame.pack(pady=(20,5), padx=10)

        self.label_1_translator = customtkinter.CTkLabel(master=self.frame_1, text="Translator")
        self.label_1_translator.pack(pady=5, padx=10)

        self.combobox_translator = customtkinter.CTkComboBox(self.frame_1, 
            state="readonly", 
            values=["Deepl", "Google"])
        
        self.combobox_translator.pack(pady=5, padx=10)

        self.label_2 = customtkinter.CTkLabel(master=self.frame_1, text="From")
        self.label_2.pack(pady=5, padx=10)

        self.combobox_from = customtkinter.CTkComboBox(
            self.frame_1, 
            state="readonly",
            values=list(deepl_lang_codes.keys()))
        self.combobox_from.pack(pady=5, padx=10)

        self.label_3 = customtkinter.CTkLabel(master=self.frame_1, text="To")
        self.label_3.pack(pady=5, padx=10)

        self.combobox_to = customtkinter.CTkComboBox(self.frame_1, 
            state="readonly",
            values=list(deepl_lang_codes.keys()))
        self.combobox_to.pack(pady=(5), padx=10)

        self.button_set_auto_mode = customtkinter.CTkButton(master=self.frame_1, text="Auto mode")
        self.button_set_auto_mode.pack(pady=(15), padx=10)

        self.button_snapshot = customtkinter.CTkButton(master=self.frame_1, text="Snapshot")
        self.button_snapshot.pack(pady=(15), padx=10)

        self.frame_metadata = customtkinter.CTkFrame(master=self)
        self.frame_metadata.pack(pady=(0,20), padx=60, fill="both", expand=True)

        self.label_metadata = customtkinter.CTkLabel(master=self.frame_metadata, text="Metadata")
        self.label_metadata.pack(pady=(20,5), padx=10)

        self.label_translation_count = customtkinter.CTkLabel(master=self.frame_metadata, text="Translation count: 0")
        self.label_translation_count.pack(pady=5, padx=10)

        self.label_translation_timeouts = customtkinter.CTkLabel(master=self.frame_metadata, text="Translation timeouts: 0")
        self.label_translation_timeouts.pack(pady=5, padx=10)

        self.frame_logs = LogsFrame(self)
        self.frame_logs.pack(pady=(0,20), padx=60, fill="both", expand=True)


class MainTKWrapper():

    def __init__(self):
        self.app = MainTKWindow()
        self.state = StateData()
        self.translation_count = 0
        self.translation_timeouts = 0
        self.translate_window_wrapper = None
        self.selectable_frame_window = None
        self.select_monitor_window = None
        self.app.button_select_frame.configure(command=self.select_frame)

        self.app.combobox_translator.configure(command=self.update_translator_combobox)
        self.app.combobox_translator.set(self.state.translator)

        self.app.combobox_from.configure(command=self.update_from_lang_combobox)
        self.app.combobox_from.set(self.state.from_lang)

        self.app.combobox_to.configure(command=self.update_to_lang_combobox)
        self.app.combobox_to.set(self.state.to_lang)

        self.app.button_set_auto_mode.configure(command=self.toggle_auto)

        self.app.button_snapshot.configure(command=self.snapshot)

        self.open_translate_window()

    def toggle_auto(self):
        if self.translate_window_wrapper:
            self.translate_window_wrapper.toggle_auto()

    def snapshot(self):
        if self.translate_window_wrapper:
            threading.Thread(target=self.snapshot_call).start()

    def snapshot_call(self):
        asyncio.run(self.translate_window_wrapper.keep_translating())

    def open_translate_window(self):
        if self.state.x1 is not None:
            from toplevel_tks.real_time_translate import TranslateWindowWrapper
            self.translate_window_wrapper = TranslateWindowWrapper(self)

    def add_log(self, log):
        self.app.frame_logs.textbox_logs.configure(state="normal") 
        self.app.frame_logs.textbox_logs.insert(tk.END, log + "\n")
        self.app.frame_logs.textbox_logs.see(tk.END)
        self.app.frame_logs.textbox_logs.configure(state="disabled") 
        self.app.frame_logs.textbox_logs.update()

    def add_translation_count(self):
        self.translation_count += 1
        self.app.label_translation_count.configure(text=f"Translation count: {self.translation_count}")

    def add_translation_timeout(self):
        self.translation_timeouts += 1
        self.app.label_translation_timeouts.configure(text=f"Translation timeouts: {self.translation_timeouts}")

    def update_from_lang_combobox(self, choice):
        self.state.from_lang = choice
        self.state.saveState()

    def update_to_lang_combobox(self, choice):
        self.state.to_lang = choice
        self.state.saveState()

    def update_display(self, choice):
        self.state.display = choice
        self.state.saveState()

    def update_translator_combobox(self, choice):
        self.state.translator = choice
        self.state.saveState()

        if choice == "Deepl":
            self.app.combobox_from.configure(values=list(deepl_lang_codes.keys()))
            self.app.combobox_to.configure(values=list(deepl_lang_codes.keys()))

            if deepl_lang_codes.get(self.state.from_lang) is None:
                from_lang = next(iter(deepl_lang_codes)) 
                self.state.from_lang = from_lang
                self.state.saveState()
                self.app.combobox_from.set(from_lang)

            if deepl_lang_codes.get(self.state.to_lang) is None:
                to_lang = next(iter(deepl_lang_codes)) 
                self.state.to_lang = to_lang
                self.state.saveState()
                self.app.combobox_to.set(to_lang)
            
        elif choice == "Google":
            self.app.combobox_from.configure(values=list(google_lang_codes.keys()))
            self.app.combobox_to.configure(values=list(google_lang_codes.keys()))

            if google_lang_codes.get(self.state.from_lang) is None:
                from_lang = next(iter(google_lang_codes)) 
                self.state.from_lang = from_lang
                self.state.saveState()
                self.app.combobox_to.set(from_lang)
            if google_lang_codes.get(self.state.to_lang) is None:
                to_lang = next(iter(google_lang_codes)) 
                self.state.to_lang = to_lang
                self.state.saveState()
                self.app.combobox_to.set(to_lang)

    def bring_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                if child.winfo_name() == 'translate_window':
                    child.state("normal")
                else:
                    child.deiconify()

    def minimize_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                if child.winfo_name() == 'translate_window':
                    child.state("withdrawn")
                else:
                    child.iconify()

    def select_frame(self):
        if self.state.display is None:
            from toplevel_tks.select_monitor import SelectMonitor
            self.select_monitor_window = SelectMonitor(self)
        else:
            self.minimize_child_windows()
            self.app.iconify()
            from toplevel_tks.selectable_frame import SelectableFrame
            self.selectable_frame_window = SelectableFrame(self)