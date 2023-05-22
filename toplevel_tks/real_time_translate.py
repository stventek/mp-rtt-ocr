import asyncio
import sys
import threading
import tkinter as tk
from collections import deque
from playwright import async_api
from toplevel_tks.text_display import TextDisplayWindowWrapper, TextDisplayWindowWrapperLinux
from utils.logger import CallBackLogger
from utils.main_tk_state import computeFrameData
from utils.ocr import OCR, printImg
from utils.translator_manager import TranslatorManager
import main_tk

class TranslateWindowWrapper:
    def __init__(self, mainTk: main_tk.MainTKWrapper):
        self.mainTk = mainTk
        self.mainTk.app.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.translator = TranslatorManager()
        self.thread_queue = deque()  
        self.logger = CallBackLogger('MainTK', self.add_log, 
            self.mainTk.state.log_level)
        self.update_label_interval = 50
        self.translate_task : asyncio.Task = None
        self.text = ""
        self.tranlated_text = ""
        if sys.platform == 'linux' or sys.platform == 'darwin':          
            self.text_display_window = TextDisplayWindowWrapperLinux(self.mainTk.app, self.mainTk)
        else:
            self.text_display_window = TextDisplayWindowWrapper(self.mainTk.app, self.mainTk)
        self.text_display_window.main_window.after(self.update_label_interval, self.update_label)
        self.active_thread = threading.Event()
        self.my_thread = threading.Thread(target=self.update_translation)
        self.my_thread.start()
        self.text_display_window.update_canvas()      
        self.text_display_window.main_window.after(50, self.check_thread)

    def check_thread(self):
        while(self.thread_queue):
            request, data = self.thread_queue.popleft()
            if request == 'add_log':
                self.mainTk.add_log(data)
            elif request == 'add_translation_timeout':
                self.mainTk.add_translation_timeout()
            elif request == 'add_translation_count':
                self.mainTk.add_translation_count()
        self.text_display_window.main_window.after(50, self.check_thread)

    def add_log(self, log):
        self.thread_queue.append(('add_log', log))

    async def translate(self, text: str):
        sanitazed_text = text.replace("\n", " ")
        translated_text = await self.translator.translate(sanitazed_text, 
            self.mainTk.state.from_lang, 
            self.mainTk.state.to_lang,
            self.mainTk.state.translator,
            self.mainTk.state.translate_timeout)
        return translated_text

    def OCR_contents(self):
        if self.mainTk.state.ocr_mode == 'Static Frame':
            x, y, w, h = computeFrameData(
                self.mainTk.state.x1,
                self.mainTk.state.y1,
                self.mainTk.state.x2,
                self.mainTk.state.y2)
            img = printImg(x, y, w, h)
        elif self.mainTk.state.ocr_mode == 'Magic Window':
            img = printImg(*self.mainTk.magic_window.window_square)
        return OCR(img)

    async def run_translate_task(self):
        done = False
        while(not done):
            try:
                text = self.OCR_contents()
                if text != "" and not text.isspace() and self.text != text:
                    self.logger.info(f"Try translate {self.mainTk.state.translator}")
                    self.tranlated_text = await self.translate(text)
                    self.text = text
                    self.logger.info("Successful translation")
                    self.thread_queue.append(('add_translation_count', None))
                    done = True
                else:
                    done = True
            except async_api.TimeoutError:
                self.thread_queue.append(('add_translation_timeout', None))
                self.logger.info("Timeout, re trying")  
                  
    async def keep_translating(self):
        try:
            self.translate_task = asyncio.create_task(self.run_translate_task())
            await self.translate_task
            self.translate_task = None
        except asyncio.CancelledError:
            self.logger.info("Task translation cancelled")  

    def update_translation(self):
        while not self.active_thread.is_set():
            if self.text_display_window.auto_mode:
                self.logger.debug("OCR check")
                asyncio.run(self.keep_translating())
            self.active_thread.wait(int(self.mainTk.state.ocr_interval) / 1000)

    def update_label(self):
        if self.text_display_window.label.get('1.0', tk.END + '-1c') != self.tranlated_text:
            self.text_display_window.label.delete('1.0', tk.END)
            self.text_display_window.label.insert(tk.END, self.tranlated_text)
        self.text_display_window.main_window.after(self.update_label_interval, self.update_label)

    def toggle_auto(self):
        self.text_display_window.auto_mode = not self.text_display_window.auto_mode
        self.text_display_window.update_canvas()
        if self.text_display_window.auto_mode: 
            self.logger.info(f"OCR scan every {int(self.mainTk.state.ocr_interval) / 1000}s")
            self.mainTk.app.button_snapshot.configure(state="disabled")
        else:
            self.mainTk.app.button_snapshot.configure(state=tk.NORMAL)

    def on_exit(self):
        self.active_thread.set()
        if self.translate_task:
            self.translate_task.cancel()
        self.my_thread.join()
        self.mainTk.app.destroy()
