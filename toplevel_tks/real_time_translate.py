import asyncio
import logging
import threading
import urllib.parse

import tkinter as tk
from collections import deque
from pynput import keyboard
from playwright import async_api

from utils.logger import CallBackLogger
from utils.main_tk_state import computeFrameData
from utils.ocr import OCR, printImg
from utils.translate_word import TranslatorManager
import main_tk

class TranslateWindow(tk.Toplevel):
    def __init__(self, root: tk.Tk):
        super().__init__(root, name="translate_window")
        self.mainTk = root
        self.width = 800
        self.height = 200
        self.configure(bg='black')
        self.wm_attributes('-topmost', True)
        self.focus()
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)
        self.geometry(f'{self.width}x{self.height}+{0}+{0}')
        self.overrideredirect(True)
        self.canvas = tk.Canvas(self, bg='black', highlightthickness=0)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH) 
        self.label = tk.Label(self.canvas, fg='white', bg='black', font=('Helvetica', 18), wraplength=self.width - 80)
        self.label.pack(fill="both", expand=tk.YES)
        self.canvas.create_window(40, 40, anchor="nw", window=self.label)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

class TranslateWindowWrapper:
    def __init__(self, mainTk: main_tk.MainTKWrapper):
        self.mainTk = mainTk
        self.mainTk.app.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.translator = TranslatorManager()
        self.thread_queue = deque()  
        self.logger = CallBackLogger('MainTK', self.add_log, 
            logging.DEBUG)
        self.update_translation_interval = 0.25
        self.update_label_interval = 50
        self.auto_mode = False
        self.translate_task : asyncio.Task = None
        self.text = ""
        self.tranlated_text = ""
        self.translate_window = TranslateWindow(self.mainTk.app)
        self.translate_window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.translate_window.after(self.update_label_interval, self.update_label)
        self.active_thread = threading.Event()
        self.my_thread = threading.Thread(target=self.update_translation)
        self.my_thread.start()
        self.update_canvas()      
        self.translate_window.after(50, self.check_thread)
        #self.hotkey_ctrl_c_t = keyboard.GlobalHotKeys({'<ctrl>+<alt>+t': self.toggle_auto_event})
        #self.hotkey_ctrl_c_t.start()

    def check_thread(self):
        while(self.thread_queue):
            request, data = self.thread_queue.popleft()
            if request == 'add_log':
                self.mainTk.add_log(data)
            elif request == 'add_translation_timeout':
                self.mainTk.add_translation_timeout()
            elif request == 'add_translation_count':
                self.mainTk.add_translation_count()
        self.translate_window.after(50, self.check_thread)

    def add_log(self, log):
        self.thread_queue.append(('add_log', log))

    async def translate(self, text: str):
        sanitazed_text = text.replace("\n", " ")
        translated_text = await self.translator.translate(sanitazed_text, 
            self.mainTk.state.from_lang, 
            self.mainTk.state.to_lang,
            self.mainTk.state.translator)
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
        flag = True
        while(flag):
            try:
                text = self.OCR_contents()
                if text != "" and not text.isspace() and self.text != text:
                    self.logger.info(f"Try translate {self.mainTk.state.translator}")
                    self.tranlated_text = await self.translate(text)
                    self.text = text
                    self.logger.info("Successful translation")
                    self.thread_queue.append(('add_translation_count', None))
                    flag = False
                else:
                    flag = False
            except async_api.TimeoutError:
                self.thread_queue.append(('add_translation_timeout', None))
                self.logger.info("Timeout, re trying")  
                  

    async def keep_translating(self):
        self.translate_task = asyncio.create_task(self.run_translate_task())
        await self.translate_task

    def update_translation(self):
        while not self.active_thread.is_set():
            if self.auto_mode:
                self.logger.debug("OCR check")
                try:
                    asyncio.run(self.keep_translating())
                except asyncio.exceptions.CancelledError:
                    print("Translation task cancelled")
            self.active_thread.wait(self.update_translation_interval)

    def update_label(self):
        self.translate_window.label.configure(text=self.tranlated_text)
        self.translate_window.after(self.update_label_interval, self.update_label)

    def update_canvas(self):
        if self.auto_mode == True:
            self.translate_window.canvas.create_oval(self.translate_window.width - 10, 40, self.translate_window.width - 40, 10, fill='green')
        else:
            self.translate_window.canvas.create_oval(self.translate_window.width - 10, 40, self.translate_window.width - 40, 10, fill='black')

    def toggle_auto(self):
        self.auto_mode = not self.auto_mode
        self.update_canvas()
        if self.auto_mode: 
            self.logger.info(f"OCR scan every {self.update_translation_interval}s")
            self.mainTk.app.button_snapshot.configure(state="disabled")
        else:
            self.mainTk.app.button_snapshot.configure(state=tk.NORMAL)

    def on_exit(self):
        self.active_thread.set()
        if self.translate_task:
            self.translate_task.cancel()
        self.my_thread.join()
        self.mainTk.app.destroy()
        #self.hotkey_ctrl_c_t.stop()
