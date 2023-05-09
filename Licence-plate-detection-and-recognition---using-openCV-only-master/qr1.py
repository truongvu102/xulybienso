import cv2
from pyzbar.pyzbar import decode

# Khởi tạo camera

cap = cv2.VideoCapture(0)

while True:
    # Đọc hình ảnh từ camera
    _, frame = cap.read()

    # Phát hiện mã QR và giải mã
    decoded_data = decode(frame)

    # Hiển thị dữ liệu giải mã được
    if decoded_data:
        print(decoded_data[0].data.decode('utf-8'))
    
    # Hiển thị hình ảnh
    cv2.imshow("QR Scanner", frame)

    # Thoát khỏi vòng lặp khi nhấn phím 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
