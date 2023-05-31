import sys
import tkinter as tk
from collections import deque
from toplevels.text_display import TextDisplayWindowWrapper, TextDisplayWindowWrapperLinux
from toplevels.translator_toplevel.translate_threadsafe_helper import TranslateThreadSafe
from utils.logger import CallBackLogger
import main_window_wrapper

class TranslateWindowWrapper:
    def __init__(self, mainTk: main_window_wrapper.MainTKWrapper):
        self.mainTk = mainTk
        self.mainTk.window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.thread_queue = deque()  
        self.logger = CallBackLogger('MainTK', self.add_log, 
            self.mainTk.state.log_level)
        self.text_display_window = self.create_text_display_window()
        self.text_display_window.update_canvas()      
        self.translate_thread_safe = TranslateThreadSafe(self.thread_queue, self.logger, self.mainTk)
        self.text_display_window.main_window.after(50, self.check_thread)

    def create_text_display_window(self):
        if sys.platform == 'linux' or sys.platform == 'darwin':
            return TextDisplayWindowWrapperLinux(self.mainTk.window, self.mainTk)
        else:
            return TextDisplayWindowWrapper(self.mainTk.window, self.mainTk)

    def check_thread(self):
        requests = {
            'add_log': lambda data: self.mainTk.window.main_tk_frame.add_log(data),
            'update_label': lambda data: self.update_label(data),
            'add_translation_timeout': lambda data: self.mainTk.window.main_tk_frame.controls_frame.group_label_metadata.add_translation_timeout(),
            'add_translation_count': lambda data: self.mainTk.window.main_tk_frame.controls_frame.group_label_metadata.add_translation_count()
        }
        while self.thread_queue:
            request, data = self.thread_queue.popleft()
            if request in requests:
                requests[request](data)
        self.text_display_window.main_window.after(50, self.check_thread)

    def add_log(self, log):
        self.thread_queue.append(('add_log', log))

    def update_label(self, translated_text):
        if self.text_display_window.label.get('1.0', tk.END + '-1c') != translated_text:
            self.text_display_window.label.delete('1.0', tk.END)
            self.text_display_window.label.insert(tk.END, translated_text)

    def toggle_auto(self):
        self.text_display_window.auto_mode = not self.text_display_window.auto_mode
        self.text_display_window.update_canvas()
        if self.text_display_window.auto_mode:
            self.translate_thread_safe.infinte_translate = True 
            self.logger.info(f"OCR scan every {int(self.mainTk.state.ocr_interval) / 1000}s")
            self.mainTk.window.main_tk_frame.controls_frame.group_label_controls.button_snapshot.configure(state="disabled")
        else:
            self.translate_thread_safe.infinte_translate = False
            self.mainTk.window.main_tk_frame.controls_frame.group_label_controls.button_snapshot.configure(state=tk.NORMAL)

    def on_exit(self):
        self.translate_thread_safe.active_thread.set()  
        self.translate_thread_safe.cancel_translate_task()
        self.translate_thread_safe.thread.join()
        self.mainTk.window.destroy()
