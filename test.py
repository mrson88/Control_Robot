import speech_recognition
import pyttsx3
from datetime import date,datetime
import os
import paho.mqtt.client as mqtt

robot_mouth=pyttsx3.init()
voices = robot_mouth.getProperty('voices')
# for i in voices:
# 	print("voices")
# 	print("ID=%s"% i.id)
# voice_id_VN="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_viVN_An"
robot_mouth.setProperty('voice',[0])
robot_ear=speech_recognition.Recognizer()
robot_ear.energy_threshold = 500
robot_brain=''

"""
Python MQTT Subscription client
Thomas Varnish (https://github.com/tvarnish), (https://www.instructables.com/member/Tango172)
Written for my Instructable - "How to use MQTT with the Raspberry Pi and ESP8266"
"""

# Don't forget to change the variables for the MQTT broker!
mqtt_username = "sondaica"
mqtt_password = "daovanson"
mqtt_topic = "esp8266"
mqtt_broker_ip = "192.168.2.14"

client = mqtt.Client()
# Set the username and password for the MQTT client
client.username_pw_set(mqtt_username, mqtt_password)

# These functions handle what happens when the MQTT client connects
# to the broker, and what happens then the topic receives a message
def on_connect(client, userdata, flags, rc):
    # rc is the error code returned when connecting to the broker
    print ("Connected!"), str(rc)
    
    # Once the client has connected to the broker, subscribe to the topic
    client.subscribe(mqtt_topic)
    
def on_message(client, userdata, msg):
    # This function is called everytime the topic is published to.
    # If you want to check each message, and do something depending on
    # the content, the code to do this should be run in this function
    
    print ("Topic: ", msg.topic + "\nMessage: " + str(msg.payload))
    
    # The message itself is stored in the msg variable
    # and details about who sent it are stored in userdata

# Here, we are telling the client which functions are to be run
# on connecting, and on receiving a message
client.on_connect = on_connect
client.on_message = on_message


# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)


# Once we have told the client to connect, let the client object run itself


while True:
	with speech_recognition.Microphone() as mic:
		print("Robot: I'm Listenning")
		audio=robot_ear.listen(mic)
	print("Robot:....")
	try:
		you=robot_ear.recognize_google(audio)
	except Exception as e:
		you=''
	print('you:'+you)

	if you=='':
		robot_brain="I can't hear you, Try again"
	elif 'hello'in you:
		robot_brain="xin chào bạn đào văn sơn"
		client.publish(mqtt_topic,"1")
	elif 'today' in you:
		today = date.today()
		robot_brain = today.strftime("%B %d, %Y")
	elif 'time' in you:
		now=datetime.now()
		robot_brain=now.strftime("%H hours %M minutes %S seconds")
	elif 'president' in you:
		robot_brain="Nguyễn Phú Trọng"
	elif 'off' in you:
		robot_brain="Tắt đèn"
		client.publish(mqtt_topic,"1")
	elif 'on' in you:
		robot_brain="Bật đèn"
		client.publish(mqtt_topic,"0")
	elif 'hi' in you:
		robot_brain="Viết chương trình và in giá trị theo công thức cho trước: Q = √([(2 * C * D)/H]) (bằng chữ: Q bằng căn bậc hai của [(2 nhân C nhân D) chia H]. Với giá trị cố định của C là 50, H là 30. D là dãy giá trị tùy biến, được nhập vào từ giao diện người dùng, các giá trị của D được phân cách bằng dấu phẩy."
	elif 'bye' in you:
		robot_brain="Bye Mr Son"
		print("robot_brain:",robot_brain)
		robot_mouth.say(robot_brain)
		robot_mouth.runAndWait()

		break

	else:
		robot_brain="I'm fine thank you"
	print("robot_brain:",robot_brain)
	robot_mouth.say(robot_brain)
	robot_mouth.runAndWait()
# client.loop_forever()
# client.disconnect()

