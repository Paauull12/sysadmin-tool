import pytesseract
from PIL import Image
import cv2


import cv2
import pytesseract
from pytesseract import Output
import numpy as np

def functionThatParsesThePicture(img):
    myconfig = r"--psm 6 --oem 3"

    file_bytes = np.frombuffer(img.read(), np.uint8)

    img_array = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if img_array is None:
        raise ValueError("The image array is empty or None.")
    
    height, width, _ = img_array.shape

    data = pytesseract.image_to_data(img_array, config=myconfig, output_type=Output.DICT)

    username = ""
    password = ""
    index = 0
    amountOfBoxes = len(data['text'])
    for i in range(amountOfBoxes):
        if float(data['conf'][i]) > 60:
            if index == 0:
                username = data['text'][i]
                index += 1
            elif index == 1:
                password = data['text'][i]
                index += 1

    return username, password

def functionThatParsesThePicture111(imgPath):
    myconfig = r"--psm 6 --oem 3"

    img = cv2.imread(imgPath)
    height, width, _ = img.shape

    data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)

    username = ""
    password = ""
    index = 0
    amountOfBoxes = len(data['text'])
    for i in range(amountOfBoxes):
        if float(data['conf'][i]) > 60:
            if index == 0:
                username = data['text'][i]
                index += 1
            elif index == 1:
                password = data['text'][i]
                index += 1

    return username, password


