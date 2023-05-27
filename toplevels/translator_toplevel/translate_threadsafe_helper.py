import asyncio
import threading
from collections import deque
from typing import Optional
from utils.logger import CallBackLogger
from utils.main_tk_state import computeFrameData
from utils.ocr import OCR, printImg
from utils.translator_manager import TranslatorManager
import main_window_wrapper

class TranslateThreadSafe:
    def __init__(self, queue: deque, logger: CallBackLogger, mainTK: main_window_wrapper.MainTKWrapper):
        self.queue = queue
        self.logger = logger
        self.mainTk = mainTK
        self.infinte_translate = False
        self.text = ''
        self.translate_task: Optional[asyncio.Task] = None
        self.translator_manager = TranslatorManager()
        self.active_thread = threading.Event()
        self.thread = threading.Thread(target=self.translation_loop)
        self.thread.start()

    async def translate(self, text: str):
        sanitazed_text = text.replace("\n", " ")
        translated_text = await self.translator_manager.translate(sanitazed_text, 
            self.mainTk.state.from_lang, 
            self.mainTk.state.to_lang,
            self.mainTk.state.translator,
            self.mainTk.state.translate_timeout)
        return translated_text
    
    async def async_translate_task(self, text):
        done = False
        while(not done):
            try:
                self.logger.info(f"Try translate {self.mainTk.state.translator}")
                tranlated_text = await self.translate(text)
                self.logger.info("Successful translation")
                self.queue.append(('add_translation_count', None))
                self.text = text
                done = True
                return tranlated_text
            except ModuleNotFoundError:
                self.logger.info("deepl-cli is not installed, it can be installed with 'pip install deepl-cli'")  
                done = True
            except asyncio.CancelledError:
                raise asyncio.CancelledError
            except :
                self.queue.append(('add_translation_timeout', None))
                self.logger.info("Timeout, re trying")  
                  
    async def run_translate_task(self, text):
        self.translate_task = asyncio.create_task(self.async_translate_task(text))
        translated_text = await self.translate_task
        self.translate_task = None
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

    def is_translation_required(self):
        text = self.OCR_contents()
        if text and not text.isspace() and self.text != text:
            return True, text
        return False, text
    
    def cancel_translate_task(self):
        if self.translate_task:
            self.logger.info("Task translation cancelled") 
            self.translate_task.cancel()
            self.translate_task = None

    def try_run_translate_task(self):
        self.logger.debug("OCR check")
        is_required, text = self.is_translation_required()
        if is_required:
            try:
                tranlated_text = asyncio.run(self.run_translate_task(text))
                if tranlated_text is not None:
                    self.queue.append(('update_label', tranlated_text))
            except asyncio.CancelledError:
                return        

    def snapshot(self):
        self.cancel_translate_task()
        self.try_run_translate_task()

    def translation_loop(self):
        while not self.active_thread.is_set():
            if self.infinte_translate:
                self.try_run_translate_task()
            self.active_thread.wait(int(self.mainTk.state.ocr_interval) / 1000) 
