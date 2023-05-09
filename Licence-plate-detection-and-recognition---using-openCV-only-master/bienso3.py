import numpy as np
import cv2
import imutils
import pytesseract
import csv
import time
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


running = True

while running:
    cap = cv2.VideoCapture(0)
    while True:
      ret, frame = cap.read()
      cv2.imshow('Camera', frame)
      if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite('anhxe.jpg', frame)
        break

    image = cv2.imread('anhxe.jpg')

    # Thay đổi kích thước của hình ảnh
    image = imutils.resize(image, width=500)


    # Chuyển đổi sang ảnh xám
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   
    # Lọc ảnh để giảm nhiễu
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Phát hiện biên cạnh sử dụng thuật toán Canny
    edged = cv2.Canny(gray, 170, 200)
  
    # Tìm các đường viền trong ảnh bằng phương pháp findContours
    cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Vẽ tất cả các đường viền lên hình ảnh
    img1 = image.copy()
    cv2.drawContours(img1, cnts, -1, (0,255,0), 3)
 
    # Sắp xếp các đường viền theo diện tích giảm dần và lấy ra 30 đường viền lớn nhất
    cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
    NumberPlateCnt = None 

    # Vẽ 30 đường viền lớn nhất lên hình ảnh
    img2 = image.copy()
    cv2.drawContours(img2, cnts, -1, (0,255,0), 3)

    # Duyệt qua 30 đường viền lớn nhất để tìm biển số xe
    count = 0
    idx =7
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        
        if len(approx) == 4:  
            NumberPlateCnt = approx 
        # Tính toán vị trí và kích thước của đối tượng hình học được phát hiện (c)
        x, y, w, h = cv2.boundingRect(c)

        # Cắt ảnh gốc để lấy phần chứa đối tượng được phát hiện
        new_img = gray[y:y + h, x:x + w]

        # Lưu ảnh đã cắt vào thư mục 'Cropped Images-Text' với tên file là idx.png
        cv2.imwrite('Cropped Images-Text/' + str(idx) + '.png', new_img)

        # Tăng biến đếm idx lên 1
        idx+=1

        break

    # Vẽ contour của đối tượng hình học được phát hiện trên ảnh gốc
    cv2.drawContours(image, [NumberPlateCnt], -1, (0,255,0), 3)

    # Hiển thị ảnh gốc kèm với contour được vẽ lên
    cv2.imshow("Final Image With Number Plate Detected", image)

    # Đường dẫn đến ảnh đã cắt
    Cropped_img_loc = 'Cropped Images-Text/7.png'

    # Hiển thị ảnh đã cắt
    cv2.imshow("Cropped Image ", cv2.imread(Cropped_img_loc))

    # Nhận dạng ký tự trên ảnh đã cắt sử dụng thư viện Tesseract với ngôn ngữ là tiếng Anh và cấu hình là '--psm 11'
    text = pytesseract.image_to_string(Cropped_img_loc, lang='eng', config='--psm 11')

    # In ra kết quả nhận dạng
    print("Biển số xe :", text)

    #import csv
    # Lấy thời gian hiện tại
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # Tạo một list chứa thông tin cần lưu
    data = [text ,current_time]

    # Mở file CSV để ghi dữ liệu vào
    with open('license_plates.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data])

    # Dừng chương trình để người dùng có thể xem kết quả
    cv2.waitKey(0)

   
    # Giải phóng tài nguyên
    cap.release()
    cv2.destroyAllWindows()
running = False
