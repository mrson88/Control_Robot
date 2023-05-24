from __future__ import division
from tkinter import *
import cv2
import os
from PIL import ImageTk, Image
import pickle
import threading
import time



def video_stream(frame):

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 35 and conf <= 100 and distance<=100:
            
            print(labels[id_])
            print(id_)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 0, 0)
            stroke = 2

            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            conf = "{0}%".format(round(100 - conf))
            count=0 
            cv2.putText(frame, str(conf), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)
            count = count + 1
            img_item = "DataSet/User."+ name + '.' + str(count) + ".jpg"
            cv2.imwrite(img_item,roi_gray)
        else:
            name = 'unknow'
            
            font = cv2.FONT_HERSHEY_SIMPLEX

            color = (255, 0, 0)
            stroke = 2
            
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

        img_item = 'my_image.png'
        cv2.imwrite(img_item, roi_gray)

        color = (255, 0, 0)
        stoke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stoke)
    # function for video streaming
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    return imgtk

    
    
