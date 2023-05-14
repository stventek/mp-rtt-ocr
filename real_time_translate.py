import asyncio
import threading
import tkinter as tk
from data import getBoundData
from pynput import keyboard
from ocr import OCR, printImg
from playwright import async_api
from translate_word import translate_Google
import urllib.parse

class RealTimeTranslate:
    def __init__(self, root: tk.Tk):
        self.data = getBoundData()
        self.root = root
        self.translate_window = tk.Toplevel(self.root)
        self.translate_window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        #self.translate_window.withdraw()
        #self.translate_window.overrideredirect(True)
        self.width = 800
        self.height = 200
        self.translate_window.geometry(f'{self.width}x{self.height}+{0}+{0}')
        self.root.geometry(f'{self.width // 2}x{self.height // 2}+{self.width}+{0}')
        self.translate_window.configure(bg='black')
        self.canvas = tk.Canvas(self.translate_window, bg='black', highlightthickness=0)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH) 
        #self.translate_window.wm_attributes('-topmost', True)
        self.translate_window.focus()
        self.label = tk.Label(self.canvas,fg='white', bg='black', font=('Helvetica', 18), wraplength=self.width - 80)
        self.label.pack(fill="both", expand=tk.YES)
        self.canvas.create_window(40, 40, anchor="nw", window=self.label)
        self.hotkey_ctrl_c_t = keyboard.GlobalHotKeys({'<ctrl>+<alt>+t': self.toggle})
        #self.hotkey_ctrl_c = keyboard.GlobalHotKeys({'<ctrl>+c': self.on_exit})
        self.active_thread = threading.Event()
        self.my_thread = threading.Thread(target=self.update_translation)
        self.update_translation_interval = 3
        self.update_label_interval = 500
        self.state = False
        self.text = ""
        self.tranlated_text = ""
        self.translate_count = 0
        self.hotkey_ctrl_c_t.start()
        self.translate_window.after(self.update_label_interval, self.update_label)
        self.my_thread.start()

    def translate(self, text: str):
        sanitazed_text = text.replace("\n", " ")
        sanitazed_text = urllib.parse.quote(sanitazed_text)
        translated_text = asyncio.run(translate_Google(sanitazed_text))
        return translated_text

    def keep_translating(self):
        while not self.active_thread.is_set():
            try:
                img = printImg(self.data)
                text = OCR(img)
                if self.text != text:
                    self.tranlated_text = self.translate(text)
                    self.translate_count += 1
                    self.text = text
                    print("translate count", self.translate_count)
                    break
            except async_api.TimeoutError:
                    print("Timeout, trying again")

    def update_translation(self):
        while not self.active_thread.is_set():
            if self.state:
                self.keep_translating()
            self.active_thread.wait(self.update_translation_interval)

    def update_label(self):
        if self.state:
            if self.tranlated_text != self.label.cget('text'):
                self.label.configure(text=self.tranlated_text)
        self.translate_window.after(self.update_label_interval, self.update_label)

    def update_canvas(self):
        if self.state == True:
            self.canvas.create_oval(self.width - 10, 40, self.width - 40, 10, fill='green')
        else:
            self.canvas.create_oval(self.width - 10, 40, self.width - 40, 10, fill='black')

    def toggle(self):
        self.state = not self.state
        self.update_canvas()

    def on_exit(self):
        self.hotkey_ctrl_c_t.stop()
        self.active_thread.set()
        self.my_thread.join()
        self.root.destroy()