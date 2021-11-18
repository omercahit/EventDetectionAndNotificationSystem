#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import threading,cv2
from sftp import *

def record(name):
    import cv2 as cv
    import time
    from datetime import datetime
    t0=time.time()
    kayit = cv2.VideoCapture(-1)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video = cv.VideoWriter(name, fourcc, 20.0, (640,  480))
    while kayit.isOpened():
        ret, frame = kayit.read()
        t1=time.time()
        num_seconds=t1-t0
        if not ret:
            print("Kamera okunamadı...")
            break
        cv.imshow("Kamera", frame)
        #frame = cv.flip(frame, 1)
        video.write(frame)
        if num_seconds>21:
            break
        if cv.waitKey(1) == ord('q'):
            break
    #kayit.release()
    video.release()
    # cv.destroyAllWindows()

############################################################################################

def save_to_dropbox(name):
    import dropbox

    class TransferData:
        def __init__(self, access_token):
            self.access_token = access_token

        def upload_file(self, file_from, file_to):
            dbx = dropbox.Dropbox(self.access_token)

            with open(file_from, 'rb') as f:
                dbx.files_upload(f.read(), file_to)

    def main():
        access_token = 'YOUR-DROPBOX-TOKEN-HERE'
        transferData = TransferData(access_token)

        file_from = name # This is name of the file to be uploaded
        file_to = '/'+name  # This is the full path to upload the file to, including name that you wish the file to be called once uploaded.

        # API v2
        transferData.upload_file(file_from, file_to)

    if __name__ == '__main__':
        main()

############################################################################################

def motion_detection_roi(r):
    
    # importing OpenCV and time library
    import cv2, time
    # importing datetime class from datetime library
    from datetime import datetime
  
    # Assigning our static_back to None
    static_back = None
        
    # List when any moving object appear
    motion_list = [ None, None ]
  
    # Time of movement
    time = []
  
    # Capturing video
    video = cv2.VideoCapture(-1)
  
    # Infinite while loop to treat stack of image as video
    while True:
        # Reading frame(image) from video
        check, frame = video.read()
  
        if r is None:
            r = cv2.selectROI(frame)
            continue
    
        # Initializing motion = 0(no motion)
        motion = 0
        
        frame_new=frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
  
        # Converting color image to gray_scale image
        gray = cv2.cvtColor(frame_new, cv2.COLOR_BGR2GRAY)
  
        # Converting gray scale image to GaussianBlur 
        # so that change can be find easily
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
  
        # In first iteration we assign the value 
        # of static_back to our first frame
        if static_back is None:
            static_back = gray
            continue
  
        # Difference between static background 
        # and current frame(which is GaussianBlur)
        diff_frame = cv2.absdiff(static_back, gray)
  
        # If change in between static background and
        # current frame is greater than 30 it will show white color(255)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
  
        # Finding contour of moving object
        cnts = cv2.findContours(thresh_frame.copy(), 
                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
  
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            motion = 1
  
            (x, y, w, h) = cv2.boundingRect(contour)
            # making green rectangle arround the moving object
            cv2.rectangle(frame_new, (x, y), (x + w, y + h), (0, 255, 0), 3)
  
        # Appending status of motion
        motion_list.append(motion)
  
        motion_list = motion_list[-2:]
  
        # Appending Start time of motion
        if motion_list[-1] == 1 and motion_list[-2] == 0:
            time.append(datetime.now())
            now=datetime.now()
            dt_string=now.strftime("%d_%m_%Y-%H_%M_%S.avi")
            i=1
            video.release()
            record(dt_string)
            
            sendtopi(dt_string)
            save_to_dropbox(dt_string)
            i=i+1
            
            motion_detection_roi(r)
            #th1.start()
            #t2.start()
  
        # Appending End time of motion
        if motion_list[-1] == 0 and motion_list[-2] == 1:
            time.append(datetime.now())

  
        # Displaying color frame with contour of motion of object
        cv2.imshow("Color Frame", frame)
  
        key = cv2.waitKey(1)
        # if q entered whole process will stop
        if key == ord('q'):
            # if something is movingthen it append the end time of movement
            if motion == 1:
                time.append(datetime.now())
            break
   
    video.release()
  
    # Destroying all the windows
    cv2.destroyAllWindows()


###########################################################################################



def motion_detection_subtract(r):
  
    # importing OpenCV and time library
    import cv2, time
    # importing datetime class from datetime library
    from datetime import datetime
  
    # Assigning our static_back to None
    static_back = None
     
    # List when any moving object appear
    motion_list = [ None, None ]
  
    # Time of movement
    time = []
  
    # Capturing video
    video = cv2.VideoCapture(-1)
  
    # Infinite while loop to treat stack of image as video
    while True:
        # Reading frame(image) from video
        check, frame = video.read()
  
        if r is None:
            r = cv2.selectROI(frame)
            continue
    
        # Initializing motion = 0(no motion)
        motion = 0
  
        # Converting color image to gray_scale image
        frame_new=frame
        frame_new[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]=255
        gray = cv2.cvtColor(frame_new, cv2.COLOR_BGR2GRAY)
  
        # Converting gray scale image to GaussianBlur 
        # so that change can be find easily
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
  
        # In first iteration we assign the value 
        # of static_back to our first frame
        if static_back is None:
            static_back = gray
            continue
  
        # Difference between static background 
        # and current frame(which is GaussianBlur)
        diff_frame = cv2.absdiff(static_back, gray)
  
        # If change in between static background and
        # current frame is greater than 30 it will show white color(255)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
  
        # Finding contour of moving object
        cnts = cv2.findContours(thresh_frame.copy(), 
                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
  
        for contour in cnts:
            if cv2.contourArea(contour) < 10000:
                continue
            motion = 1
  
            (x, y, w, h) = cv2.boundingRect(contour)
            # making green rectangle arround the moving object
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
  
        # Appending status of motion
        motion_list.append(motion)
  
        motion_list = motion_list[-2:]
  
        # Appending Start time of motion, calling the record and save functions
        if motion_list[-1] == 1 and motion_list[-2] == 0:
            time.append(datetime.now())
            now=datetime.now()
            dt_string=now.strftime("%d_%m_%Y-%H_%M_%S.avi")
            i=1
            video.release()
            record(dt_string)

            sendtopi(dt_string)
            save_to_dropbox(dt_string)
            i=i+1
            
            motion_detection_subtract(r)

        # Appending End time of motion
        if motion_list[-1] == 0 and motion_list[-2] == 1:
            time.append(datetime.now())
  
  
        # Displaying color frame with contour of motion of object
        cv2.imshow("Color Frame", frame)
  
        key = cv2.waitKey(1)
        # if q entered whole process will stop
        if key == ord('q'):
            # if something is movingthen it append the end time of movement
            if motion == 1:
                time.append(datetime.now())
            break
  
 
    video.release()
  
    # Destroying all the windows
    cv2.destroyAllWindows()

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import form

class Pencere(QMainWindow, form.Ui_uii):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.kapat)
        
    def kapat(self):
        r = None
        if self.comboBox.currentText()=='Çıkar':
            motion_detection_subtract(r)
        else:
            motion_detection_roi(r)

app = QApplication(sys.argv)
pencere = Pencere()
pencere.show()
sys.exit(app.exec_())