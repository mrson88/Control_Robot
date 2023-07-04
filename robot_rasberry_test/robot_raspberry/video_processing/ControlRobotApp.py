import time
import pyshine as ps
import imutils
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from control_robot_ui_test import Ui_MainWindow
import argparse
from PyQt5 import  QtGui, QtWidgets
import cv2
#from handtracker import detect_hand
from tflite_reg import start
from talk_person import TalkPerson
from mobilenetssd import do_detect

import numpy as np
import continuous_threading
from decide_control import Decide_Control
from Facerec_QT.face_rec import FaceRecognition,read_db,write_db
class_id=0
confidence=0
distance=0
xcentre=0
"""1
try:
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
except Exception as e:
    print('Warning...', e)

"""


class ControlRobotWindow(QMainWindow, Ui_MainWindow,TalkPerson,Decide_Control):
    # change_pixmap_signal = pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        TalkPerson.__init__(self)
        Decide_Control.__init__(self)
        self.ui = Ui_MainWindow()
        self.setupUi(self)
        self.pushButton_play.clicked.connect(self.loadImage)
        self.pushButton_pause.clicked.connect(self.savePhoto)
        self.tmp = None  # Will hold the temporary image for display
        self.brightness_value_now = 0  # Updated brightness value
        self.blur_value_now = 0  # Updated blur value
        self.fps = 0
        self.started = False
        self.show()
        self.finish=True
        self.recognition_on=True
        self.registration_data = None
        self.frame_height = 480
        self.frame_width = 640
        self.face_recognition = FaceRecognition(0.7, self.frame_height, self.frame_width)
        self.pushButton_register.clicked.connect(self.register_button_func)
        self.pushButton_quit.clicked.connect(self.close)


    def loadImage(self):
        """ This function will load the camera device, obtain the image
            and set it to label using the setPhoto function
        """
        if self.started:
            self.started = False
            self.pushButton_play.setText('Start')
        else:
            self.started = True
            self.pushButton_play.setText('Stop')

        cam = True  # True for webcam
        if cam:
            vid = cv2.VideoCapture(0)
            
        else:
            vid = cv2.VideoCapture('video.mp4')

        cnt = 0
        frames_to_count = 20
        st = 0
        fps = 0

        while (vid.isOpened()):
            QtWidgets.QApplication.processEvents()
            _, self.image = vid.read()
            #self.image = imutils.resize(self.image, height=640, width=480)

            
            try:
                pass
                
            except Exception as e:
                pass

            if cnt == frames_to_count:
                try:  # To avoid divide by 0 we put it in try except
                    #print(frames_to_count / (time.time() - st), 'FPS')
                    self.fps = round(frames_to_count / (time.time() - st))

                    st = time.time()
                    cnt = 0
                except:
                    pass

            cnt += 1

            self.update()
            key = cv2.waitKey(1) & 0xFF
            if self.started == False:
                print('Loop break')
                break

    def setPhoto(self, image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """
        self.tmp = image
        #image = imutils.resize(image, width=480)
        
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        

    def update(self):
        global confidence
        global class_id
        global xcentre
        global prev_frame_time
        """ This function will update the photo according to the
            current values of blur and brightness and set it to photo label.
        """
        # img = self.changeBrightness(self.image, self.brightness_value_now)
        # img = self.changeBlur(img, self.blur_value_now)

        # Here we add display text to the image
        
        text = str(time.strftime("%H:%M:%S %p"))
        img = ps.putBText(self.image, text, text_offset_x=20, text_offset_y=10, vspace=10, hspace=3,
                          font_scale=0.5, background_RGB=(228, 20, 222), text_RGB=(255, 255, 255))

        if self.checkBox_2.checkState()==0:
            frame_detect,class_id,confidence,xcentre=start(img)
            #post_video_stream(img)
            

            #frame_detect=detect_hand(frame_detect)
            gray = cv2.cvtColor(frame_detect, cv2.COLOR_BGR2GRAY)
            processed_frame, ids = self.face_recognition.process_frame(frame_detect, self.recognition_on, self.registration_data)
            """
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.15,
                minNeighbors=7,
                minSize=(80, 80),
                flags=cv2.CASCADE_SCALE_IMAGE)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame_detect, (x, y), (x + w, y + h), (10, 228, 220), 5)
            if len(faces)>0 and self.finish:
                print('face')
                self.finish=False
                self.talk_robot_AI()
                self.finish=True
                """
                
            self.setPhoto(frame_detect)
            second=time.strftime('%S')
            
            #if int(second)%2==0:
            #self.dokc()

            #thead_dicide=continuous_threading.PeriodicThread(20,self.dicide)
            #thead_dicide.start()
            #thead_dicide.stop()
        else:
            frame_detect ,class_id,confidence,xcentre= do_detect(img)
            #frame_detect=detect_hand(frame_detect_raw)
            self.setPhoto(frame_detect)

    def savePhoto(self):
        """ This function will save the image"""
        self.filename = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        cv2.imwrite(self.filename, self.tmp)

        print('Image saved as:', self.filename)

    def talk_robot_AI(self):
        thead_talk=continuous_threading.ContinuousThread(target=self.listen)
        thead_talk.start()
        thead_talk.stop()
    
    def register_button_func(self):
        data=read_db()
        print(len(data))
        print(data)
        self.registration_data = [len(data), self.name.text()]

        


            
            
# video_path = "ssd_mobilenet_model/videos/test3.mp4"
# video_path = 0


app = QApplication(sys.argv)
video_show = ControlRobotWindow()
video_show.show()
sys.exit(app.exec())
