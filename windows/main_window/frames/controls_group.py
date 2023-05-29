import customtkinter as ck
from windows.main_window.frames.custom_label_frame import CustomLabelFrame
from main_window_wrapper import MainTKWrapper
from utils.translator_manager import deepl_lang_codes, google_lang_codes
import tkinter as tk
import pytesseract

class ControlsGroup(CustomLabelFrame):
    def __init__(self, mainW: MainTKWrapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mainW = mainW

        self.translation_count = 0
        self.translation_timeouts = 0
        
        self.grid(row=0, column=0, sticky='ewns', pady=(0,10), padx=(0,10))

        self.frame_group.grid_columnconfigure(0, weight=1)
        self.frame_group.grid_columnconfigure(1, weight=1)

        self.button_snapshot = ck.CTkButton(master=self.frame_group, text="Snapshot")
        self.button_snapshot.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        self.button_set_auto_mode = ck.CTkButton(master=self.frame_group, text="Auto mode")
        self.button_set_auto_mode.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        self.label_mode = ck.CTkLabel(master=self.frame_group, text="OCR Mode")
        self.label_mode.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.combobox_mode = ck.CTkComboBox(self.frame_group,
            state="readonly", 
            values=["Static Frame", "Magic Window"])
        
        self.combobox_mode.grid(row=2, column=1, padx=10, pady=10, sticky='w')
        self.combobox_mode.set("Static Frame")

        self.label_1_translator = ck.CTkLabel(master=self.frame_group, text="Translator")
        self.label_1_translator.grid(row=3, column=0, padx=10, pady=10, sticky='e')

        self.combobox_translator = ck.CTkComboBox(self.frame_group, 
            state="readonly", 
            values=["Deepl", "Google"])
        
        self.combobox_translator.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        self.label_trained_data = ck.CTkLabel(master=self.frame_group, text="Trained data")
        self.label_trained_data.grid(row=4, column=0, padx=10, pady=10, sticky='e')

        self.combobox_trained_data = ck.CTkComboBox(self.frame_group, 
            state="readonly", 
            values=pytesseract.get_languages())
        
        self.combobox_trained_data.grid(row=4, column=1, padx=10, pady=10, sticky='w')

        self.label_2 = ck.CTkLabel(master=self.frame_group, text="From")
        self.label_2.grid(row=5, column=0, padx=10, pady=10, sticky='e')

        self.combobox_from = ck.CTkComboBox(
            self.frame_group, 
            state="readonly",
            values=[])
        self.combobox_from.grid(row=5, column=1, padx=10, pady=10, sticky='w')

        self.label_3 = ck.CTkLabel(master=self.frame_group, text="To")
        self.label_3.grid(row=6, column=0, padx=10, pady=10, sticky='e')

        self.combobox_to = ck.CTkComboBox(
            self.frame_group, 
            state="readonly",
            values=[])
        self.combobox_to.grid(row=6, column=1, padx=10, pady=10, sticky='w')

        self.button_advance = ck.CTkButton(master=self.frame_group, text="Advance Settings")
        self.button_advance.grid(row=7, column=1, padx=10, pady=10, sticky='w')

        self._update_languages_list()
        self.button_set_auto_mode.configure(command=self.mainW.toggle_auto)
        self.button_snapshot.configure(command=self.snapshot)
        self.combobox_translator.configure(command=self._update_translator_combobox)
        self.combobox_translator.set(self.mainW.state.translator)
        self.combobox_trained_data.configure(command=self._update_trained_data_combobox)
        self.combobox_trained_data.set(self.mainW.state.trained_data)
        self.combobox_from.configure(command=self._update_from_lang_combobox)
        self.combobox_from.set(self.mainW.state.from_lang)
        self.combobox_to.configure(command=self._update_to_lang_combobox)
        self.combobox_to.set(self.mainW.state.to_lang)
        self.button_advance.configure(command=self.mainW.open_advance)
        self.combobox_mode.configure(command=self.mainW.change_ocr_mode)
        self.combobox_mode.set(self.mainW.state.ocr_mode)
 
    def snapshot(self):
        self.button_snapshot.configure(state=tk.DISABLED)
        self.master.after(1000, lambda: self.button_snapshot.configure(state=tk.NORMAL))
        self.mainW.snapshot()

    def _update_trained_data_combobox(self, choice):
        self.mainW.state.trained_data = choice
        self.mainW.state.saveState()
        
    def _update_from_lang_combobox(self, choice):
        self.mainW.state.from_lang = choice
        self.mainW.state.saveState()

    def _update_to_lang_combobox(self, choice):
        self.mainW.state.to_lang = choice
        self.mainW.state.saveState()

    def _update_translator_combobox(self, choice):
        self.mainW.state.translator = choice
        self.mainW.state.saveState()
        self._update_languages_list()

    def _update_languages_list(self):
        if self.mainW.state.translator == "Deepl":
            self.combobox_from.configure(values=list(deepl_lang_codes.keys()))
            self.combobox_to.configure(values=list(deepl_lang_codes.keys()))

            if deepl_lang_codes.get(self.mainW.state.from_lang) is None:
                from_lang = next(iter(deepl_lang_codes)) 
                self.mainW.state.from_lang = from_lang
                self.mainW.state.saveState()
                self.combobox_from.set(from_lang)

            if deepl_lang_codes.get(self.mainW.state.to_lang) is None:
                to_lang = next(iter(deepl_lang_codes)) 
                self.mainW.state.to_lang = to_lang
                self.mainW.state.saveState()
                self.combobox_to.set(to_lang)
        elif self.mainW.state.translator  == "Google":
            self.combobox_from.configure(values=list(google_lang_codes.keys()))
            self.combobox_to.configure(values=list(google_lang_codes.keys()))

            if google_lang_codes.get(self.mainW.state.from_lang) is None:
                from_lang = next(iter(google_lang_codes)) 
                self.mainW.state.from_lang = from_lang
                self.mainW.state.saveState()
                self.combobox_to.set(from_lang)
            if google_lang_codes.get(self.mainW.state.to_lang) is None:
                to_lang = next(iter(google_lang_codes)) 
                self.mainW.state.to_lang = to_lang
                self.mainW.state.saveState()
                self.combobox_to.set(to_lang)