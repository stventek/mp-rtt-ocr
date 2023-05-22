from utils.lang_codes import deepl_lang_codes, google_lang_codes
from deepl import DeepLCLI
from googletrans import Translator as GoogleTranslator

class TranslatorManager():

    async def translate(self, text, from_lang, to_lang, translator, timeout):
        if translator == "Deepl":
            deepl = DeepLCLI(deepl_lang_codes[from_lang], deepl_lang_codes[to_lang], timeout=int(timeout))
            return await deepl.translate_async(text)
        elif translator == "Google":
            google = GoogleTranslator()
            return google.translate(text, 
                src=google_lang_codes[from_lang], 
                dest=google_lang_codes[to_lang], timeout=int(timeout)).text