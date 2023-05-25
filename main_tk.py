import asyncio
import threading
import customtkinter
from customtkinter import ThemeManager
from frames.maintk_frame import MainTKFrame
from utils.get_displays import get_displays
from utils.main_tk_state import StateData
from utils.translator_manager import deepl_lang_codes, google_lang_codes
import tkinter as tk

customtkinter.set_default_color_theme("custom_theme.json")
appearance_mode = customtkinter.AppearanceModeTracker()

class MainTKWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Real Time OCR translator")
        self.width = 900
        self.height = 600
        self.geometry(f"{self.width}x{self.height}")

        self.main_tk_frame = MainTKFrame(self, fg_color=ThemeManager.theme["CTk"]["fg_color"])
        self.main_tk_frame.pack(fill="both", expand=True)

class MainTKWrapper():

    def __init__(self):
        self.app = MainTKWindow()
        self.state = StateData()
        self.translation_count = 0
        self.translation_timeouts = 0
        self.translate_window_wrapper = None
        self.selectable_frame_window = None
        self.select_monitor_window = None
        self.magic_window = None
        self.initialize_app()

    def initialize_app(self):
        from toplevel_tks.real_time_translate import TranslateWindowWrapper
        self.setup_main_tk_frame()
        self.update_languages_list()
        self.translate_window_wrapper = TranslateWindowWrapper(self)
        self.open_magic_window()
        self.open_debug_group()
        customtkinter.set_appearance_mode(self.state.theme.lower())

    def setup_main_tk_frame(self):
        main_frame = self.app.main_tk_frame

        main_frame.button_set_auto_mode.configure(command=self.toggle_auto)
        main_frame.button_snapshot.configure(command=self.snapshot)
        main_frame.button_select_frame.configure(command=self.select_frame)
        main_frame.combobox_display.configure(command=self.update_display)
        main_frame.combobox_display.set(self.state.display['choice'])
        main_frame.combobox_translator.configure(command=self.update_translator_combobox)
        main_frame.combobox_translator.set(self.state.translator)
        main_frame.combobox_from.configure(command=self.update_from_lang_combobox)
        main_frame.combobox_from.set(self.state.from_lang)
        main_frame.combobox_to.configure(command=self.update_to_lang_combobox)
        main_frame.combobox_to.set(self.state.to_lang)
        main_frame.button_advance.configure(command=self.open_advance)
        main_frame.combobox_mode.configure(command=self.change_ocr_mode)
        main_frame.combobox_mode.set(self.state.ocr_mode)
        main_frame.switch_frame_magic.configure(command=self.unframe_magic)

    def update_theme(self):
        customtkinter.set_appearance_mode(self.state.theme.lower())

    def update_text_win_opacity(self, val):
        self.translate_window_wrapper.text_display_window.child_toplevel.app.attributes('-alpha', val / 100)

    def update_log_level(self):
        self.translate_window_wrapper.logger.setLevel(self.state.log_level)
        for handler in self.translate_window_wrapper.logger.handlers:
            handler.setLevel(self.state.log_level)

    def open_debug_group(self):
        if self.state.debug_mode == 'on':
            self.app.main_tk_frame.group_label_logs.pack(fill='both', expand=True, side='left', padx=10, pady=10)
            self.app.geometry(f"{self.app.width}x{self.app.height}")
        else:
            self.app.main_tk_frame.group_label_logs.pack_forget()
            self.app.geometry(f"{435}x{self.app.height}")

    def unframe_magic(self):
        if self.magic_window:
            self.magic_window.unframe_window()

    def change_ocr_mode(self, choice):
        if self.state.ocr_mode != choice:
            if choice == 'Magic Window':
                self.state.ocr_mode = 'Magic Window'
                self.open_magic_window()
                self.state.saveState()
            elif choice == 'Static Frame':
                self.magic_window.destroy()
                self.state.ocr_mode = 'Static Frame'
                self.state.saveState()
                
    def open_magic_window(self):
        if self.state.ocr_mode == 'Magic Window':
            from toplevel_tks.magic_window import MagicWindow
            self.magic_window = MagicWindow(self)
    
    def open_advance(self):
        from toplevel_tks.advance_settings import AdvanceSettings
        self.advance_settings_wrapper = AdvanceSettings(self) 

    def toggle_auto(self):
        if self.state.ocr_mode != 'Static Frame' or self.state.x1 is not None:
            self.translate_window_wrapper.toggle_auto()

    def snapshot(self):
        if self.state.ocr_mode != 'Static Frame' or self.state.x1 is not None:
            if self.translate_window_wrapper.translate_task:
                self.translate_window_wrapper.translate_task.cancel()
            threading.Thread(target=self.snapshot_call).start()

    def snapshot_call(self):
        asyncio.run(self.translate_window_wrapper.keep_translating())

    def add_log(self, log):
        self.app.main_tk_frame.textbox_logs.configure(state="normal") 
        self.app.main_tk_frame.textbox_logs.insert(tk.END, log + "\n")
        self.app.main_tk_frame.textbox_logs.see(tk.END)
        self.app.main_tk_frame.textbox_logs.configure(state="disabled") 
        self.app.main_tk_frame.textbox_logs.update()

    def add_translation_count(self):
        self.translation_count += 1
        self.app.main_tk_frame.label_translation_count.configure(text=f"Translation count: {self.translation_count}")

    def add_translation_timeout(self):
        self.translation_timeouts += 1
        self.app.main_tk_frame.label_translation_timeouts.configure(text=f"Translation timeouts: {self.translation_timeouts}")

    def update_from_lang_combobox(self, choice):
        self.state.from_lang = choice
        self.state.saveState()

    def update_to_lang_combobox(self, choice):
        self.state.to_lang = choice
        self.state.saveState()

    def update_display(self, choice):
        self.state.display = get_displays()[int(choice) - 1]
        self.state.display["choice"] = choice
        self.state.saveState()

    def update_translator_combobox(self, choice):
        self.state.translator = choice
        self.state.saveState()
        self.update_languages_list()

    def update_languages_list(self):
        if self.state.translator == "Deepl":
            self.app.main_tk_frame.combobox_from.configure(values=list(deepl_lang_codes.keys()))
            self.app.main_tk_frame.combobox_to.configure(values=list(deepl_lang_codes.keys()))

            if deepl_lang_codes.get(self.state.from_lang) is None:
                from_lang = next(iter(deepl_lang_codes)) 
                self.state.from_lang = from_lang
                self.state.saveState()
                self.app.main_tk_frame.combobox_from.set(from_lang)

            if deepl_lang_codes.get(self.state.to_lang) is None:
                to_lang = next(iter(deepl_lang_codes)) 
                self.state.to_lang = to_lang
                self.state.saveState()
                self.app.main_tk_frame.combobox_to.set(to_lang)
            
        elif self.state.translator  == "Google":
            self.app.main_tk_frame.combobox_from.configure(values=list(google_lang_codes.keys()))
            self.app.main_tk_frame.combobox_to.configure(values=list(google_lang_codes.keys()))

            if google_lang_codes.get(self.state.from_lang) is None:
                from_lang = next(iter(google_lang_codes)) 
                self.state.from_lang = from_lang
                self.state.saveState()
                self.app.main_tk_frame.combobox_to.set(from_lang)
            if google_lang_codes.get(self.state.to_lang) is None:
                to_lang = next(iter(google_lang_codes)) 
                self.state.to_lang = to_lang
                self.state.saveState()
                self.app.main_tk_frame.combobox_to.set(to_lang)


    def bring_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                if child.winfo_name() == 'text_display_win_parent':
                    child.state("normal")
                elif child.winfo_name() == 'text_display_child':
                    child.state("normal")
                elif child.winfo_name() == 'magic_window':
                    child.state("normal")
                else:
                    child.deiconify()

    def minimize_child_windows(self):
        for child in self.app.winfo_children():
            if isinstance(child, tk.Toplevel):
                if child.winfo_name() == 'text_display_win_parent':
                    child.state("withdrawn")
                elif child.winfo_name() == 'text_display_child':
                    child.state("withdrawn")
                elif child.winfo_name() == 'magic_window':
                    child.state("withdrawn")
                else:
                    child.iconify()

    def select_frame(self):
        if self.state.display['top'] is None:
            answer = tk.messagebox.askquestion(title="Display selection", message="Is display number 1 correct?")
            if answer == 'yes':
                self.update_display('1')
            else:
                return
        self.minimize_child_windows()
        self.app.iconify()
        from toplevel_tks.selectable_frame import SelectableFrame
        self.selectable_frame_window = SelectableFrame(self)