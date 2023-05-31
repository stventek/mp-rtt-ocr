import asyncio
import threading
import customtkinter
from utils.main_tk_state import StateData
import tkinter as tk

customtkinter.set_default_color_theme("custom_theme.json")
appearance_mode = customtkinter.AppearanceModeTracker()

class MainTKWrapper():

    def __init__(self):
        self.state = StateData()
        from windows.main_window.main_window import MainTKWindow
        self.window = MainTKWindow(self)
        self.translate_window_wrapper = None
        self.selectable_frame_window = None
        self.select_monitor_window = None
        self.magic_window = None
        self.initialize_app()

    def initialize_app(self):
        from toplevels.translator_toplevel.translate_toplevel import TranslateWindowWrapper
        self.translate_window_wrapper = TranslateWindowWrapper(self)
        self.open_magic_window()
        self.open_debug_group()
        customtkinter.set_appearance_mode(self.state.theme.lower())

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
            self.window.main_tk_frame.group_label_logs.pack(fill='both', expand=True, side='left', padx=10, pady=10)
            self.window.geometry(f"{self.window.width}x{self.window.height}")
        else:
            self.window.main_tk_frame.group_label_logs.pack_forget()
            self.window.geometry(f"{435}x{self.window.height}")

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
            from toplevels.magic_window import MagicWindow
            self.magic_window = MagicWindow(self)
    
    def open_advance(self):
        from toplevels.advance_settings import AdvanceSettings
        self.advance_settings_wrapper = AdvanceSettings(self) 

    def toggle_auto(self):
        if self.state.ocr_mode != 'Static Frame' or self.state.x1 is not None:
            self.translate_window_wrapper.toggle_auto()

    def snapshot(self):
        if self.state.ocr_mode != 'Static Frame' or self.state.x1 is not None:
            self.translate_window_wrapper.translate_thread_safe.cancel_translate_task()
            threading.Thread(target=self.translate_window_wrapper.translate_thread_safe.snapshot).start()

    def bring_child_windows(self):
        for child in self.window.winfo_children():
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
        for child in self.window.winfo_children():
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
                self.window.main_tk_frame.controls_frame.update_display('1')
            else:
                return
        self.minimize_child_windows()
        self.window.iconify()
        from toplevels.selectable_frame import SelectableFrame
        self.selectable_frame_window = SelectableFrame(self)