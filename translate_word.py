import asyncio
from playwright.async_api import async_playwright
from lang_codes import deepl_lang_codes, google_lang_codes

class Translator():
    deepl_lang_codes = deepl_lang_codes
    google_lang_codes = google_lang_codes

    def translate(self, word, from_lang, to_lang, translator):
        if translator == "Deepl":
            return asyncio.run(self.translate_Deepl(word, from_lang, to_lang))
        elif translator == "Google":
            return asyncio.run(self.translate_Google(word, from_lang, to_lang))

    async def translate_Deepl(self, word, from_lang, to_lang):
        async with async_playwright() as p:
            url = 'https://www.deepl.com/translator#en/es/' + word
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            page.set_default_timeout(10000)
            await page.goto(url)
            await page.wait_for_selector('div[aria-labelledby="translation-results-heading"][role="textbox"] > p > span > span')
            p_locator = page.locator('div[aria-labelledby="translation-results-heading"][role="textbox"] > p')
            paragraphs = await p_locator.all_text_contents()
            text = '\n'.join(paragraphs)
            await browser.close()
            return text
        
    async def translate_Google(self, word, from_lang, to_lang):
        async with async_playwright() as p:
            url = f'https://translate.google.com/?hl=es&sl=en&tl=es&text={word}&op=translate'
            browser = await p.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            page.set_default_timeout(10000)
            await page.goto(url)
            await page.wait_for_selector('c-wiz[aria-labelledby="ucj-4"] > div > div > div > div > span > span > span')
            p_locator = page.locator('c-wiz[aria-labelledby="ucj-4"] > div > div > div > div > span > span > span')
            paragraphs = await p_locator.all_text_contents()
            text = ' '.join([line for line in paragraphs if line != ""])
            await browser.close()
            return text
