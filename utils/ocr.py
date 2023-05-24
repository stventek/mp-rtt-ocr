import mss
import numpy as np
import pytesseract
from PIL import Image

def printImg(x,y,w,h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {
            "top": y, 
            "left": x,  
            "width": w,
            "height": h,
        }
        return np.array(sct.grab(monitor))[:, :, 0]

def OCR(image):
    text : str = pytesseract.image_to_string(image)
    return text
