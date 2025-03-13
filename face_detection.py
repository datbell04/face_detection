import cv2
import face_recognition
import os

import numpy as np

# load anh tu kho
path = "pic2"
imageList = []
classNames = []
myList = os.listdir(path)

print(myList)

for a in myList:
    print(a)
    curImg = cv2.imread(f"{path}/{a}")
    imageList.append(curImg)
    classNames.append(os.path.splitext(a)[0])

print(len(imageList))
print(classNames)



# encoding

def encodeFace(imageList):
    encodeList = []
    for img in imageList :
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encodes = face_recognition.face_encodings(img)
        if len(encodes) > 0:
            encodeList.append(encodes[0])  # Lấy encoding đầu tiên nếu có khuôn mặt
        else:
            print("Không tìm thấy khuôn mặt trong một ảnh!")
    return encodeList


encodeListKnow = encodeFace(imageList)
print("Successfull!")


# triển khai webcam

cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    if not ret :
        print("không thể truy cập webcam")
        break

    frameS = cv2.resize(frame, (0,0),None, fx = 0.5, fy = 0.5)
    frameS = cv2.cvtColor(frameS,cv2.COLOR_BGR2RGB)

    # xác dịnh vi tri va ma hoa mat tren cam
    faceCurFrame = face_recognition.face_locations(frameS)
    encodefaceCurFrame = face_recognition.face_encodings(frameS,faceCurFrame)

    for encodecurFace, faceLoc in zip(encodefaceCurFrame,faceCurFrame) :
        matches = face_recognition.compare_faces(encodeListKnow,encodecurFace)
        face_dis = face_recognition.face_distance(encodeListKnow,encodecurFace)
        print(face_dis)
        matchIndex = np.argmin(face_dis) # đẩy về index của giá trị nhỏ nhất


        if face_dis[matchIndex] < 0.5:
            name = classNames[matchIndex].upper()
        else :
            name = "unknown"

        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 2, x2 * 2, y2 * 2, x1 * 2  # Scale lại kích thước
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("webcam",frame)
    if cv2.waitKey(1) == ord("q") :
        break
cap.release()
cv2.destroyAllWindows()