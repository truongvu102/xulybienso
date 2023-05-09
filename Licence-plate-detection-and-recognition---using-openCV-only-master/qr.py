import cv2
from pyzbar import pyzbar
import RPi.GPIO as GPIO
import time

# khởi tạo GPIO cho servo
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
pwm=GPIO.PWM(7, 50)
pwm.start(0)

# định nghĩa hàm điều khiển servo
def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(7, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(7, False)
    pwm.ChangeDutyCycle(0)

# định nghĩa danh sách QR code cần quét
qr_codes = ["vu quang truong", "vu van hanh", "nhom 7"]

# khởi tạo camera
url = 'http://192.168.43.1:4747/video'
cap = cv2.VideoCapture(url)

while True:
    # đọc hình ảnh từ camera
    ret, frame = cap.read()

    # tìm kiếm QR code trong hình ảnh
    decodedObjects = pyzbar.decode(frame)

    # kiểm tra xem QR code có nằm trong danh sách cần quét không
    for obj in decodedObjects:
        if obj.data.decode() in qr_codes:
            # nếu có thì điều khiển servo quay 90 độ
            SetAngle(90)
            time.sleep(1)
            SetAngle(0)

    # hiển thị hình ảnh
    cv2.imshow("QR Code Scanner", frame)

    # chờ bấm phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# giải phóng các tài nguyên và kết thúc chương trình
cap.release()
cv2.destroyAllWindows()
pwm.stop()
GPIO.cleanup()
