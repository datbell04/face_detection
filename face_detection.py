import cv2
import face_recognition
import os
import requests
import numpy as np
from tkinter import messagebox, Tk
import time

# Ẩn cửa sổ chính tkinter
root = Tk()
root.withdraw()

# API config
API_URL = "http://localhost:5000/images"
BASE_URL = "http://localhost:5000"

def get_images_from_api():
    response = requests.get(API_URL)
    if response.status_code != 200:
        print("Không thể lấy dữ liệu ảnh từ API!")
        return []
    return response.json()

# Tải ảnh từ API
imageList = []
classNames = []

for img_data in get_images_from_api():
    img_url = BASE_URL + img_data["path"]
    name = img_data["filename"]
    print(name)

    img_response = requests.get(img_url)
    if img_response.status_code == 200:
        img_array = np.asarray(bytearray(img_response.content), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        imageList.append(img)
        classNames.append(os.path.splitext(name)[0])
    else:
        print(f"Lỗi khi tải ảnh: {img_url}")

print(f"Tải thành công {len(imageList)} ảnh!")
print(classNames)

# Encode ảnh
def encodeFace(imageList):
    encodeList = []
    for img in imageList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])
        else:
            print("Không tìm thấy khuôn mặt trong một ảnh!")
    return encodeList

encodeListKnow = encodeFace(imageList)
print("Encode thành công!")

# Mở webcam
cap = cv2.VideoCapture(0)
shown_name = None
message_shown = False

start_time = time.time()  # Ghi lại thời gian bắt đầu
delay_seconds = 3        # Chờ 5 giây sau khi mở camera

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể truy cập webcam")
        break

    frameS = cv2.resize(frame, (0, 0), None, fx=0.5, fy=0.5)
    frameS = cv2.cvtColor(frameS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(frameS)
    encodefaceCurFrame = face_recognition.face_encodings(frameS, faceCurFrame)

    for encodecurFace, faceLoc in zip(encodefaceCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodecurFace)
        face_dis = face_recognition.face_distance(encodeListKnow, encodecurFace)
        print(face_dis)
        matchIndex = np.argmin(face_dis)

        if face_dis[matchIndex] < 0.5:
            name = classNames[matchIndex].upper()
            label = "PASS"
        else:
            name = "unknown"
            label = "FAIL"

        # Chỉ hiển thị messagebox sau khi đã chạy được 5 giây và chỉ hiển thị một lần
        if not message_shown and time.time() - start_time > delay_seconds:
            if label == "PASS":
                messagebox.showinfo("Xác thực", f"{name}: PASS")
            else:
                messagebox.showwarning("Xác thực", "FAIL: Không tìm thấy khuôn mặt")
            message_shown = True  # Đảm bảo chỉ hiển thị một lần

        # Vẽ khung quanh khuôn mặt
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
