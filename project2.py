
import face_recognition
import cv2

imgAnbimbim = face_recognition.load_image_file("/pic2/obama.jpg")
imgAnbimbim = cv2.cvtColor(imgAnbimbim,cv2.COLOR_BGR2RGB)
# chuyen doi anh tu mau bgr thanh rgb



imgcheck = face_recognition.load_image_file("D:\\workspace\\python\\python_face\\pic\\anbimbimCheck.jpg")
imgcheck = cv2.cvtColor(imgcheck,cv2.COLOR_BGR2RGB)

# xac dinh vi tri khuon mat
faceLoc = face_recognition.face_locations(imgAnbimbim)[0]
print(faceLoc) # y1,x2, y2,x1


#ma hoa hinh anh
encodeAnbimbim = face_recognition.face_encodings(imgAnbimbim)[0]
cv2.rectangle(imgAnbimbim,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
#anh , toa do x1 , y1  , toa do x2, y2 , mau , do day


faceCheck = face_recognition.face_locations(imgcheck)[0]
print(faceCheck)

encodeCheck = face_recognition.face_encodings(imgcheck)[0]
cv2.rectangle(imgcheck,(faceCheck[3],faceCheck[0]),(faceCheck[1],faceCheck[2]),(0,0,0),2)

result = face_recognition.compare_faces([encodeAnbimbim],encodeCheck)
faceDis = face_recognition.face_distance([encodeAnbimbim],encodeCheck)
# khoang cach cang ngan thi cang dung
print(result,faceDis)
cv2.putText(imgcheck, f"{result}{round(faceDis[0],2)}",(50,50),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)


cv2.imshow("anBimBim",imgAnbimbim)
cv2.imshow("obama",imgcheck)
cv2.waitKey()
# nhan vao phim de tat
