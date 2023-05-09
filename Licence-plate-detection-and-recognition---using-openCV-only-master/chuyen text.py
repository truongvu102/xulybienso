import pytesseract
import numpy as np
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'
# Đường dẫn đến file ảnh
#image_path = "path/to/image.png"

# Đọc ảnh và chuyển đổi thành đối tượng Image
image = cv2.imread('image.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("1 - Grayscale Conversion", gray)
cv2.waitKey(0)
# Chuyển đổi ảnh thành văn bản bằng pytesseract
text = pytesseract.image_to_string(gray, lang='eng',config='--psm 11')

# In ra văn bản
print(text)