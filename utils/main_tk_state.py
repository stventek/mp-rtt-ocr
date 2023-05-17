import json

def computeFrameData(x1, y1, x2, y2):
    w = abs(x2 - x1)
    h = abs(y2 - y1)
    x = min(x1, x2)
    y = min(y1, y2)
    return (x, y, w, h,)

class StateData:
    def __init__(self):
        data = self._loadData()
        self.x1 = data.get('x1')
        self.x2 = data.get('x2')
        self.y1 = data.get('y1')
        self.y2 = data.get('y2')
        self.translator = data.get('translator') or 'Deepl'
        self.from_lang = data.get('from_lang') or 'English'
        self.to_lang = data.get('to_lang') or 'Spanish'
        self.display = data.get('display') or {"top":None,"left":None,"width":None,"height":None, "choice":1}
        self.ocr_interval = data.get('ocr_interval') or 250
        self.debug_mode = data.get('debug_mode') or 'on'
        self.translate_timeout = data.get('translate_timeout') or 8000
        self.log_level = data.get('log_level') or 'DEBUG'

    def _loadData(self) -> dict:
        try:
            with open('data.json') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def to_dict(self ):
        return {
            'x1': self.x1, 
            'x2': self.x2,
            'y1': self.y1,
            'y2': self.y2,
            'translator': self.translator,
            'to_lang': self.to_lang,
            'from_lang': self.from_lang,
            'display': self.display,
            'ocr_interval': self.ocr_interval,
            'debug_mode': self.debug_mode,
            'translate_timeout': self.translate_timeout,
            'log_level': self.log_level
        }

    def saveState(self):
        with open('data.json', 'w') as f:
            json.dump(self.to_dict(), f)