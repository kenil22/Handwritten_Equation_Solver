
import os
for fol in os.listdir('extracted_images'):
    if len(os.listdir(os.path.join('extracted_images',fol))) > 4000:
        for file in os.listdir(os.path.join('extracted_images',fol)):
            os.remove(os.path.join(os.path.join('extracted_images',fol, file)))
            if len(os.listdir(os.path.join('extracted_images',fol))) <= 4000:
                break



# from PIL import Image
# import pytesseract

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# im = Image.open("equation_images\\savedimage.jpeg")

# text = pytesseract.image_to_string(im, lang = 'eng')

# print(text)




# import paddleocr
# from paddleocr import PaddleOCR
# import cv2

# cropped_img = cv2.imread('equation_images\\test9.png')

# Paddle = PaddleOCR(lang='en',  det_db_score_mode='slow', use_dilation=True,  show_log=False, use_angle_cls=True)

# output = Paddle.ocr(cropped_img)
# print(output)




