import cv2
import mss
import numpy as np
import pytesseract

def printImg(x,y,w,h):
    with mss.mss() as sct:
        # The screen part to capture
        monitor = {
            "top": y, 
            "left": x,  
            "width": w,
            "height": h,
        }
        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def OCR(image):
    text : str = pytesseract.image_to_string(image)
    return text
