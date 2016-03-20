import numpy as np
import os
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
if face_cascade.empty(): raise Exception("your face_cascade is empty. are you sure, the path is correct ?")

def get_images_and_labels(path): 
    folder_paths = [os.path.join(path, f) for f in os.listdir(path)] 
    images = [] 
    labels = []
    name={}
    name[-1]="?????"
    i=0 
    for folder_path in folder_paths:
        list_image=[os.path.join(folder_path,f) for f in os.listdir(folder_path)] 
        for image_path in  list_image:
            image = cv2.imread(image_path)
            gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
            #resized=cv2.resize(gray,(100,100)) 
            images.append(gray) 
            labels.append(i)
            name[i]=(os.listdir(path)[i])
            #cv2.imshow("Adding faces to traning set...", image) 
            #cv2.waitKey(50)
        i+=1
    return images, labels, name
def trainning(img_folder):
    recognizer = cv2.createLBPHFaceRecognizer()
    img,lab,name=get_images_and_labels(img_folder)
    recognizer.train(np.array(img),np.array(lab))
    return name,recognizer
def recognise_from_image(img,recognizer, name):
    gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    face=face_cascade.detectMultiScale(gray,
                scaleFactor=1.5,
                minNeighbors=5,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE)
    for (x,y,w,h) in face:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            img_predict=gray[y+2:y+h-2,x+2:x+w-2]
            #resized=cv2.resize(img_predict,(100,100)) 
            nbr_predicted, conf = recognizer.predict(img_predict)
            cv2.putText(img,str(name[nbr_predicted]+'  '+str(conf)),(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,250,0),2)
def recognise_from_webcam(id_divice,recognizer,name):
    capture = cv2.VideoCapture(id_divice)
    while (capture.isOpened()):
        r,img=capture.read()
        recognise_from_image(img, recognizer, name)
        cv2.imshow('WebCam',img)
        cv2.waitKey(1)
def recognise_from_video(video,recognizer,name):
    capture = cv2.VideoCapture(video)
    while (capture.isOpened()):
        r,img=capture.read()
        recognise_from_image(img, recognizer, name)
        cv2.imshow('Video',img)
        cv2.waitKey(10)
#main
name,recognizer=trainning('Anh')

#recognise_from_video('video.mp4', recognizer, name)
recognise_from_webcam(0, recognizer, name)    
   


            
            
            
            
            
            
            
            
            

