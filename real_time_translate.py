import threading
import tkinter as tk
from pynput import keyboard
import main_tk
from ocr import OCR, printImg
from playwright import async_api
from translate_word import Translator
import urllib.parse

class RealTimeTranslate:
    def __init__(self, mainTk: main_tk.MainTK):
        self.mainTk = mainTk
        self.translate_window = tk.Toplevel(self.mainTk.app)
        self.translate_window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.mainTk.app.protocol("WM_DELETE_WINDOW", self.on_exit)
        #self.translate_window.withdraw()
        #self.translate_window.overrideredirect(True)
        self.width = 800
        self.height = 200
        self.translate_window.geometry(f'{self.width}x{self.height}+{0}+{0}')
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
        self.update_translation_interval = 0.25
        self.update_label_interval = 50
        self.state = False
        self.text = ""
        self.tranlated_text = ""
        self.hotkey_ctrl_c_t.start()
        self.translate_window.after(self.update_label_interval, self.update_label)
        self.my_thread.start()
        self.translator = Translator()

    def translate(self, text: str):
        sanitazed_text = text.replace("\n", " ")
        sanitazed_text = urllib.parse.quote(sanitazed_text)
        translated_text = self.translator.translate(sanitazed_text, 
            self.mainTk.combobox_from.get(), 
            self.mainTk.combobox_to.get(),
            self.mainTk.combobox_translator.get())
        return translated_text

    def keep_translating(self):
        while not self.active_thread.is_set() and self.state:
            try:
                img = printImg(self.mainTk.data)
                text = OCR(img)
                if text != "" and not text.isspace() and self.text != text:
                    self.mainTk.logger.info(f"Try translate {self.mainTk.combobox_translator.get()}")
                    self.tranlated_text = self.translate(text)
                    self.mainTk.add_translation_count()
                    self.text = text
                    self.mainTk.logger.info("Successful translation")
                    break
                else:
                    break
            except async_api.TimeoutError:
                    self.mainTk.add_translation_timeout()
                    self.mainTk.logger.info("Timeout, re trying")

    def update_translation(self):
        while not self.active_thread.is_set():
            if self.state:
                self.keep_translating()
                self.mainTk.logger.debug("OCR check")
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
        if self.state: self.mainTk.logger.info(f"OCR scan every {self.update_translation_interval}s")

    def on_exit(self):
        self.hotkey_ctrl_c_t.stop()
        self.active_thread.set()
        self.my_thread.join()
        self.mainTk.app.destroy()
