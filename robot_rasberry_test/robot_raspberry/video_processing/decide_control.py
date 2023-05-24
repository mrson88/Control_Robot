import time
import RPi.GPIO as GPIO
import control_robot as ag
class Decide_Control:
    def __init__(self):
        self.distance=0
        self.finish_control=True
        self.confidence=0
        self.class_id=0
        self.xcentre=0
        self.resW=320
        self.resH=240
        
    #do khoang cach vat the
    def dokc(self):
        try:
            GPIO.setmode(GPIO.BCM)
            # Khởi tạo 2 biến chứa GPIO ta sử dụng
            GPIO_TRIGGER = 23
            GPIO_ECHO = 24
            # Thiết lập GPIO nào để gửi tiến hiệu và nhận tín hiệu
            GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
            GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
            # Khai báo này ám chỉ việc hiện tại không gửi tín hiệu điện
            # qua GPIO này, kiểu kiểu ngắt điện ấy
            GPIO.output(GPIO_TRIGGER, False)
            # Cái này mình cũng không rõ, nhưng họ bảo là để khởi động cảm biến
            time.sleep(0.1)               
            # Kích hoạt cảm biến bằng cách ta nháy cho nó tí điện rồi ngắt đi luôn.
            GPIO.output(GPIO_TRIGGER, True)
            time.sleep(0.00001)
            GPIO.output(GPIO_TRIGGER, False)

            # Đánh dấu thời điểm bắt đầu
            start = time.time()
            while GPIO.input(GPIO_ECHO)==0:
                start = time.time()
            # Bắt thời điểm nhận được tín hiệu từ Echo
            while GPIO.input(GPIO_ECHO)==1:
                stop = time.time()

            # Thời gian từ lúc gửi tín hiêu
            elapsed = stop-start

            # Distance pulse travelled in that time is time
            # multiplied by the speed of sound (cm/s)
            self.distance = elapsed * 34000
            self.distance = self.distance / 2
                
            
        finally:
                # Reset GPIO settings
            GPIO.cleanup()

    def dicide(self):

        if (self.class_id==15 ) and int(self.confidence*100)>50 :
            if self.finish_control:
                #print('nguoi')
                if self.distance>100 and (self.xcentre-int(self.resW)/2<60) and (self.xcentre-int(self.resW)/2 )>-60:
                    self.finish_control=False
                    ag.forward()

                    #print('tien len')
                    self.finish_control=True
                elif self.distance<=100 and self.distance>35 :
                    self.finish_control=False
                    if (self.xcentre-int(self.resW)/2)>-60 and (self.xcentre-int(self.resW)/2)<60:
                        
                        ag.chao()
                        self.finish_control=True
                    elif (self.xcentre-int(self.resW)/2>60) :
                        
                        ag.turn_left()
                        #print('re trai')
                        self.finish_control=True
                    elif (self.xcentre-int(self.resW)/2<-60) :
                        
                        ag.turn_right()
                        #print('re phai')
                        self.finish_control=True
                elif self.distance<=35 :
                    pass
                    #print('di lui')
                    #finish=True
                
        else :
            #print('k phai nguoi')
            if self.distance>=40 and self.finish_control:
                self.finish_control=False
                ag.forward()
                #print('tien len')
                self.finish_control=True
            elif self.distance<=40 and self.distance>=25 and self.finish_control:
                self.finish_control=False
                ag.turn_left()
                #print('re trai')
                self.finish_control=True
            elif self.distance<=25 and self.finish_control:
                self.finish_control=False
                ag.backward()
                #print('di lui')
                self.finish_control=True
