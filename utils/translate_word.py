from playwright.async_api import async_playwright
from translate import Translator
from utils.lang_codes import deepl_lang_codes, google_lang_codes
import urllib.parse
class TranslatorManager():

    async def translate(self, word, from_lang, to_lang, translator):
        if translator == "Deepl":
            return await self.translate_Deepl(
                word, 
                deepl_lang_codes[from_lang], 
                deepl_lang_codes[to_lang])
        elif translator == "Google":
            return await self.translate_Google(
                word, 
                google_lang_codes[from_lang], 
                google_lang_codes[to_lang])

    async def translate_Deepl(self, word, from_lang, to_lang):
        word = urllib.parse.quote(word)
        async with async_playwright() as p:
            url = f'https://www.deepl.com/translator#{from_lang}/{to_lang}/{word}'
            browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote",
                "--window-size=1920,1080",
            ])
            context = await browser.new_context()
            page = await context.new_page()
            page.set_default_timeout(10000)
            await page.goto(url)
            await page.route(
                "**/*",
                lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "other"] else route.continue_(),
            )
            await page.wait_for_selector('div[aria-labelledby="translation-results-heading"][role="textbox"] > p > span > span')
            p_locator = page.locator('div[aria-labelledby="translation-results-heading"][role="textbox"] > p')
            paragraphs = await p_locator.all_text_contents()
            text = '\n'.join(paragraphs)
            await browser.close()
            return text
        
    async def translate_Google(self, word, from_lang, to_lang):
        word = urllib.parse.quote(word)
        async with async_playwright() as p:
            url = f'https://translate.google.com/?hl=es&sl={from_lang}&tl={to_lang}&text={word}&op=translate'
            browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--no-zygote",
                "--window-size=1920,1080",
            ])
            context = await browser.new_context()
            page = await context.new_page()
            await page.route(
                "**/*",
                lambda route: route.abort() if route.request.resource_type in ["image", "media", "font", "other"] else route.continue_(),
            )
            page.set_default_timeout(10000)
            await page.goto(url)
            await page.wait_for_selector('c-wiz[aria-labelledby="ucj-4"] > div > div > div > div > span > span > span')
            p_locator = page.locator('c-wiz[aria-labelledby="ucj-4"] > div > div > div > div > span > span > span')
            paragraphs = await p_locator.all_text_contents()
            text = ' '.join([line for line in paragraphs if line != ""])
            await browser.close()
            return text
