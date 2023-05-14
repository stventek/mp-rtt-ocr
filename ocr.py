
import cv2
import numpy as np
import pyautogui
import pytesseract

def printImg(boundData):
    img =  pyautogui.screenshot(
        region=(boundData.x, boundData.y, boundData.width, boundData.height))
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img

def OCR(image):
    text : str = pytesseract.image_to_string(image)
    return text
