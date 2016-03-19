'''
Created on Jan 15, 2016

@author: JuniorK
'''
import cv2
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if face_cascade.empty(): raise Exception("your face_cascade is empty. are you sure, the path is correct ?")
recognizer = cv2.createLBPHFaceRecognizer()
capture = cv2.VideoCapture(0)
i=0
while (capture.isOpened()):
    r,im=capture.read()
    gray = cv2.cvtColor(im,    cv2.COLOR_BGR2GRAY)
    face= face_cascade.detectMultiScale(gray,
            scaleFactor=1.5,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE)
    for (x,y,w,h) in face:
        cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
        #cv2.putText(im,'xx',(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,250,0),2)
        if (cv2.waitKey(1)&0xFF==ord('a')):
            cv2.imwrite('Anh/Ngoc/Ngoc{0}.jpg'.format(i),im[y+2:y+h-2,x+2:x+w-2])
            i+=1
            cv2.imshow("Pattern",im[y+2:y+h-2,x+2:x+w-2])
    cv2.imshow('WebCam',im)
    cv2.waitKey(1)
