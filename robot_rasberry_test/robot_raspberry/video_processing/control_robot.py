from __future__ import division
import time
from threading import Thread, Lock
cur_angle_mutex = Lock()
i2c_mutex = Lock()

# Import the PCA9685 module.
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
pwm.set_pwm_freq(60)

move_delay = 0.005
step_delay = 0.01

leg1_offset = [20,20,10]
leg2_offset = [0,10,20]
leg3_offset = [0,20,10]
leg4_offset = [20,20,10]

front_lateral = 50
front_parallel = 90
front_lateral_add = -25

back_lateral = 130
back_parallel = 90
back_lateral_add = 25

footup = 135
footdown = 70

pincer_up = 120
pincer_down = 140

leg1_footdown = footdown
leg2_footdown = footdown
leg3_footdown = footdown
leg4_footdown = footdown

leg_formation = 0

channel_cur = [90,90,90,90,90,90,90,90,90,90,90,90]


def main():
    global leg_formation
    leg_formation=1
    #pinsetup()
    begin()
    while True:
        forward()

    
def begin():
    global leg_formation
    #Move Left Side
    leg1(89,89,89) #leftside
    time.sleep(0.05)
    leg2(89,89,89)
    time.sleep(0.05)
    leg3(89,89,89)#rightside
    time.sleep(0.05)
    leg4(89,89,89)
    time.sleep(0.05)

    time.sleep(2)

    leg1(front_parallel,footdown,pincer_down) #leftside
    #time.sleep(0.1)
    leg2(back_parallel,footdown,pincer_down)
    #time.sleep(0.1)
    leg3(back_parallel,footdown,pincer_down)#rightside
    #time.sleep(0.1)
    leg4(front_parallel,footdown,pincer_down)
    #time.sleep(0.1)

    leg_formation = 1
def setServo(channel,angle):
    if(angle<0):
        angle = 0
    elif(angle>180):
        angle = 180
    
    i2c_mutex.acquire()
    Thread(target=pwm.set_pwm(channel,0,(int)((angle*2.5)+150)))
    i2c_mutex.release()

def setServo_invert(channel,angle):
    if(angle<0):
        angle = 0
    elif(angle>180):
        angle = 180

    i2c_mutex.acquire()
    Thread(target=pwm.set_pwm(channel,0,(int)((angle*-2.5)+600)))
    i2c_mutex.release()

def leg1(angle1,angle2,angle3):
    angle1 = angle1+leg1_offset[0]
    angle2 = angle2+leg1_offset[1]
    angle3 = angle3+leg1_offset[2]

    while(channel_cur[0] != angle1 or channel_cur[1] != angle2 or channel_cur[2] != angle3 ):
        ##ANGLE1
        if angle1 > channel_cur[0]:
            channel_cur[0] = channel_cur[0] +1
            setServo_invert(0,channel_cur[0])
        elif angle1 < channel_cur[0]:
            channel_cur[0] = channel_cur[0] -1
            setServo_invert(0,channel_cur[0])

        ##ANGLE2
        if angle2 > channel_cur[1]:
            channel_cur[1] = channel_cur[1] +1
            setServo(1,channel_cur[1])
        elif angle2 < channel_cur[1]:
            channel_cur[1] = channel_cur[1] -1
            setServo(1,channel_cur[1])

        ##ANGLE3
        if angle3 > channel_cur[2]:
            channel_cur[2] = channel_cur[2] +1
            setServo(2,channel_cur[2])
        elif angle3 < channel_cur[2]:
            channel_cur[2] = channel_cur[2] -1
            setServo(2,channel_cur[2])
        
        time.sleep(move_delay)

def leg2(angle1,angle2,angle3):
    angle1 = angle1+leg2_offset[0]
    angle2 = angle2+leg2_offset[1]
    angle3 = angle3+leg2_offset[2]

    while(channel_cur[3] != angle1 or channel_cur[4] != angle2 or channel_cur[5] != angle3 ):
    ##ANGLE1
        if angle1 > channel_cur[3]:
            channel_cur[3] = channel_cur[3] +1
            setServo_invert(3,channel_cur[3])
        elif angle1 < channel_cur[3]:
            channel_cur[3] = channel_cur[3] -1
            setServo_invert(3,channel_cur[3])

        ##ANGLE2
        if angle2 > channel_cur[4]:
            channel_cur[4] = channel_cur[4] +1
            setServo_invert(4,channel_cur[4])
        elif angle2 < channel_cur[4]:
            channel_cur[4] = channel_cur[4] -1
            setServo_invert(4,channel_cur[4])
       
        ##ANGLE3
        if angle3 > channel_cur[5]:
            channel_cur[5] = channel_cur[5] +1
            setServo_invert(5,channel_cur[5])
        elif angle3 < channel_cur[5]:
            channel_cur[5] = channel_cur[5] -1
            setServo_invert(5,channel_cur[5])
        
        time.sleep(move_delay)
        
def leg3(angle1,angle2,angle3):
    angle1 = angle1+leg3_offset[0]
    angle2 = angle2+leg3_offset[1]
    angle3 = angle3+leg3_offset[2]

    while(channel_cur[6] != angle1 or channel_cur[7] != angle2 or channel_cur[8] != angle3 ):
    ##ANGLE1
        if angle1 > channel_cur[6]:
            channel_cur[6] = channel_cur[6] +1
            setServo(6,channel_cur[6])
        elif angle1 < channel_cur[6]:
            channel_cur[6] = channel_cur[6] -1
            setServo(6,channel_cur[6])

        ##ANGLE2
        if angle2 > channel_cur[7]:
            channel_cur[7] = channel_cur[7] +1
            setServo(7,channel_cur[7])
        elif angle2 < channel_cur[7]:
            channel_cur[7] = channel_cur[7] -1
            setServo(7,channel_cur[7])

        ##ANGLE3
        if angle3 > channel_cur[8]:
            channel_cur[8] = channel_cur[8] +1
            setServo(8,channel_cur[8])
        elif angle3 < channel_cur[8]:
            channel_cur[8] = channel_cur[8] -1
            setServo(8,channel_cur[8])

        time.sleep(move_delay)

def leg4(angle1,angle2,angle3):
    angle1 = angle1+leg4_offset[0]
    angle2 = angle2+leg4_offset[1]
    angle3 = angle3+leg4_offset[2]

    while(channel_cur[9] != angle1 or channel_cur[10] != angle2 or channel_cur[11] != angle3 ):
    ##ANGLE1
        if angle1 > channel_cur[9]:
            channel_cur[9] = channel_cur[9] +1
            setServo(9,channel_cur[9])
        elif angle1 < channel_cur[9]:
            channel_cur[9] = channel_cur[9] -1
            setServo(9,channel_cur[9])

        ##ANGLE2
        if angle2 > channel_cur[10]:
            channel_cur[10] = channel_cur[10] +1
            setServo_invert(10,channel_cur[10])
        elif angle2 < channel_cur[10]:
            channel_cur[10] = channel_cur[10] -1
            setServo_invert(10,channel_cur[10])

        ##ANGLE3
        if angle3 > channel_cur[11]:
            channel_cur[11] = channel_cur[11] +1
            setServo_invert(11,channel_cur[11])
        elif angle3 < channel_cur[11]:
            channel_cur[11] = channel_cur[11] -1
            setServo_invert(11,channel_cur[11])

        time.sleep(move_delay)
def forward():

    global leg_formation
    print('tien len')
    if(leg_formation == 1):

        #we always lift the leg in a parallel side. Assuming forward is called after begin(), which makes the left side legs parallel and right side legs lateral
        #lift leg1
        leg1(front_parallel,footup,pincer_down)
        time.sleep(step_delay)
        #move leg1 to lateral position
        leg1(front_lateral,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg1 down 
        leg1(front_lateral,footdown,pincer_up)
        time.sleep(step_delay)

        #send leg2 to lateral, and leg4 to parallel, keep leg3 in lateral

        t1 = Thread(target=leg1, args=(front_lateral,footdown,pincer_down))
        t2 = Thread(target=leg2, args=(back_lateral,footdown,pincer_down))
        t3 = Thread(target=leg3, args=(back_lateral+back_lateral_add,footdown,pincer_up))
        t4 = Thread(target=leg4, args=(front_parallel,footdown,pincer_down))
        
        t2.start()
        t3.start()
        t4.start()
        t1.start()
        
        t2.join()
        t3.join()
        t4.join()
        t1.join()
    

        #lift leg3 and bring to parallel position

        #lift
        leg3(back_lateral+back_lateral_add,footup,pincer_down)
        time.sleep(step_delay)
        #move leg3 to parallel position
        leg3(back_parallel,footup,pincer_down)
        time.sleep(step_delay)
        #bring leg3 down
        leg3(back_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now right side legs are parallel and left side legs are lateral

        

    if (leg_formation == 2):
        #lift leg4
        leg4(front_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #move leg4 to lateral position
        leg4(front_lateral,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg4 down
        leg4(front_lateral,footdown,pincer_up)
        time.sleep(step_delay)
        
        

        # sending leg3 to lateral, and leg1 to parallel
        t4 = Thread(target=leg4, args=(front_lateral,footdown,pincer_down))
        t3 = Thread(target=leg3, args=(back_lateral,footdown,pincer_down))
        t2 = Thread(target=leg2, args=(back_lateral+back_lateral_add,footdown,pincer_up))
        t1 = Thread(target=leg1, args=(front_parallel,footdown,pincer_down))
        
        t3.start()
        t2.start()
        t1.start()
        t4.start()
        
        t3.join()
        t2.join()
        t1.join()
        t4.join()
        time.sleep(step_delay)

        #lift leg2 and bring to parallel position
        leg2(back_lateral+back_lateral_add,footup,pincer_up)
        time.sleep(step_delay)
        #move leg2 to lateral position
        leg2(back_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg2 down
        leg2(back_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now left side legs are parallel and right side legs are lateral


    if(leg_formation == 1):
        leg_formation = 2
    elif(leg_formation == 2):
        leg_formation = 1

def backward():
    global leg_formation
    print('lui xuong')
    if(leg_formation == 1):
        #we always lift the leg in a parallel side. Assuming forward is called after begin(), which makes the left side legs parallel and right side legs lateral
        #lift leg2
        leg2(back_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #move leg2 to lateral position
        leg2(back_lateral,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg2 down 
        leg2(back_lateral,footdown,pincer_down)
        time.sleep(step_delay)

        #send leg1 to lateral, and leg3 to parallel,
        t1 = Thread(target=leg1, args=(front_lateral,footdown,pincer_down))
        t3 = Thread(target=leg3, args=(back_parallel,footdown,pincer_down))
        t4 = Thread(target=leg4, args=(front_lateral+front_lateral_add,footdown,pincer_down))

        t1.start()
        t3.start()
        t4.start()

        t1.join()
        t3.join()
        t4.join()
  

        #lift leg4 and bring to parallel position

        #lift
        leg4(front_lateral+front_lateral_add,footup,pincer_up)
        time.sleep(step_delay)
        #move leg3 to parallel position
        leg4(front_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg3 down
        leg4(front_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now right side legs are parallel and left side legs are lateral

    if (leg_formation == 2):
        #lift leg3
        leg3(back_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #move leg3 to lateral position
        leg3(back_lateral,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg4 down
        leg3(back_lateral,footdown,pincer_down)
        time.sleep(step_delay)

        
        t4 = Thread(target=leg4, args=(front_lateral,footdown,pincer_down))
        t2 = Thread(target=leg2, args=(back_parallel,footdown,pincer_down))
        t1 = Thread(target=leg1, args=(front_lateral+front_lateral_add,footdown,pincer_down))
        t4.start()
        t2.start()
        t1.start()
        
        t4.join()
        t2.join()
        t1.join()
        time.sleep(step_delay)

        #lift leg1 and bring to parallel position
        leg1(front_lateral+front_lateral_add,footup,pincer_up)
        time.sleep(step_delay)
        #move leg1 to lateral position
        leg1(front_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg1 down
        leg1(front_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now left side legs are parallel and right side legs are lateral
    if(leg_formation == 1):
        leg_formation = 2
    elif(leg_formation == 2):
        leg_formation = 1
    


def turn_left():
    global leg_formation
    print('re trai')
    if(leg_formation == 1):
        #we always lift the leg in a parallel side. Assuming forward is called after begin(), which makes the left side legs parallel and right side legs lateral
        #lift leg1
        leg2(back_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #move leg1 to lateral position
        leg2(back_lateral,footup,pincer_up)
        time.sleep(step_delay)

        #send leg2 to lateral, and leg4 to parallel, keep leg3 in lateral
        t1 = Thread(target=leg1, args=(front_lateral,footdown,pincer_down))
        t3 = Thread(target=leg3, args=(back_lateral+back_lateral_add,footdown,pincer_down))
        t4 = Thread(target=leg4, args=(front_parallel,footdown,pincer_down))

        t1.start()
        t3.start()
        t4.start()

        #bring leg1 down
        leg2(back_lateral,footdown,pincer_down)
        time.sleep(step_delay)

        t1.join()
        t3.join()
        t4.join()


        #lift leg3 and bring to parallel position

        #lift
        leg3(back_lateral+back_lateral_add,footup,pincer_up)
        time.sleep(step_delay)
        #move leg3 to parallel position
        leg3(back_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg3 down
        leg3(back_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now right side legs are parallel and left side legs are lateral

        

    if (leg_formation == 2):
        #lift leg4
        leg4(front_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #move leg4 to lateral position
        leg4(front_lateral,footup,pincer_up)
        time.sleep(step_delay)

        # sending leg3 to lateral, and leg1 to parallel
        t3 = Thread(target=leg3, args=(back_lateral,footdown,pincer_down))
        t2 = Thread(target=leg2, args=(back_parallel,footdown,pincer_down))
        t1 = Thread(target=leg1, args=(front_lateral+front_lateral_add,footdown,pincer_down))
        t3.start()
        t2.start()
        t1.start() 

        #bring leg4 down
        leg4(front_lateral,footdown,pincer_down)

        t3.join()
        t2.join()
        t1.join()
        time.sleep(step_delay)

        #lift leg1 
        leg1(front_lateral+front_lateral_add,footup,pincer_up)
        time.sleep(step_delay)
        #move leg1 to prallel position
        leg1(front_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg1 down
        leg1(front_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now left side legs are parallel and right side legs are lateral


    if(leg_formation == 1):
        leg_formation = 2
    elif(leg_formation == 2):
        leg_formation = 1


def turn_right():
    global leg_formation
    print('re phai')
    if(leg_formation == 1):
        #we always lift the leg in a parallel side. Assuming forward is called after begin(), which makes the left side legs parallel and right side legs lateral
        #lift leg1
        leg1(front_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #move leg1 to lateral position
        leg1(front_lateral,footup,pincer_up)
        time.sleep(step_delay)

        #send leg2 to lateral, and leg4 to lateral+, and leg3 parallel
        t2 = Thread(target=leg2, args=(back_lateral,footdown,pincer_down))
        t3 = Thread(target=leg3, args=(back_parallel,footdown,pincer_down))
        t4 = Thread(target=leg4, args=(front_lateral+front_lateral_add,footdown,pincer_down))

        t2.start()
        t3.start()
        t4.start()

        #bring leg1 down
        leg1(front_lateral,footdown,pincer_down)
        time.sleep(step_delay)

        t2.join()
        t3.join()
        t4.join()


        #lift leg4 and bring to parallel position

        #lift leg 4
        leg4(front_lateral+front_lateral_add,footup,pincer_up)
        time.sleep(step_delay)
        #move leg4 to parallel position
        leg4(front_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg4 down
        leg4(front_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now right side legs are parallel and left side legs are lateral

        

    if (leg_formation == 2):
        #lift leg3
        leg3(back_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #move leg4 to lateral position
        leg3(back_lateral,footup,pincer_up)
        time.sleep(step_delay)

        # sending leg1 to lateral, and leg4 to lateral and leg2 to lateral+
        t1 = Thread(target=leg1, args=(front_parallel,footdown,pincer_down))
        t4 = Thread(target=leg4, args=(front_lateral,footdown,pincer_down))
        t2 = Thread(target=leg2, args=(back_lateral+back_lateral_add,footdown,pincer_down))
        t1.start()
        t4.start()
        t2.start() 

        #bring leg3 down
        leg3(back_lateral,footdown,pincer_down)

        t1.join()
        t4.join()
        t2.join()
        time.sleep(step_delay)

        #lift leg2
        leg2(back_lateral+back_lateral_add,footup,pincer_up)
        time.sleep(step_delay)
        #move leg1 to prallel position
        leg2(back_parallel,footup,pincer_up)
        time.sleep(step_delay)
        #bring leg1 down
        leg2(back_parallel,footdown,pincer_down)
        time.sleep(step_delay)

        #now left side legs are parallel and right side legs are lateral


    if(leg_formation == 1):
        leg_formation = 2
    elif(leg_formation == 2):
        leg_formation = 1
def chao():
    global leg_formation
    
    if (leg_formation == 1):
        forward()
        print('chao ban')
    #lift leg4
        leg4(front_lateral,footup,pincer_up-30)
        time.sleep(step_delay)
        leg4(front_parallel,footup,pincer_up-30)
        time.sleep(step_delay)
        #move leg4 to lateral position
        leg4(front_lateral,footup,pincer_up-30)
        time.sleep(step_delay)
        leg4(front_parallel,footup,pincer_up-30)
        time.sleep(step_delay)
        leg4(front_lateral,footup,pincer_up-30)
        time.sleep(step_delay)
        #bring leg4 down
        leg4(front_lateral,footdown,pincer_down)
        time.sleep(step_delay)
        
    elif (leg_formation == 2):
        print('chao lai')
        leg4(front_lateral,footup,pincer_up-30)
        time.sleep(step_delay)
        leg4(front_parallel,footup,pincer_up-30)
        time.sleep(step_delay)
        #move leg4 to lateral position
        leg4(front_lateral,footup,pincer_up-30)
        time.sleep(step_delay)
        leg4(front_parallel,footup,pincer_up-30)
        time.sleep(step_delay)
        leg4(front_lateral,footup,pincer_up-30)
        time.sleep(step_delay)
        #bring leg4 down
        leg4(front_lateral,footdown,pincer_down)
        time.sleep(step_delay)
    if(leg_formation == 1):
        leg_formation = 2


if __name__ == '__main__':
    main()