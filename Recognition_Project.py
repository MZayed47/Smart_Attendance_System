import cv2
import numpy as np
import face_recognition
import os
import csv
from time import gmtime, strftime
from datetime import datetime
from PIL import ImageGrab


yy = strftime("%d-%b-%Y_%H-%M", gmtime())


# Source Images

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)



# Image Names

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(classNames)



# Face Encodings

def findEncodings(images):
    encodeList = []
    
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnown = findEncodings(images)
print('Encoding Complete')
print("Number of Records: ",len(encodeListKnown))


# Webcam Launch

cap = cv2.VideoCapture(0)


frame_num = 0

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    frame_num += 1

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

    person_path = os.path.join(os.getcwd(), 'detections', 'person_' + yy)
    isdir = os.path.isdir(person_path)
    if not isdir:
        os.mkdir(person_path)

    for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name,'\n')

            final_path = os.path.join(person_path, 'frame_' + str(frame_num) + '_' + name)

            y1,x2,y2,x1 = faceLoc
            y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX,0.7,(255,255,255),2)

            cv2.imwrite(final_path + '.jpg', img)


    cv2.imshow('Webcam',img)
    cv2.waitKey(1)







