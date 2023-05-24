import cv2
import requests
import io
import socket
import struct
import time
import picamera
import sys
def post_video_stream(frame):
    
    url = "http://192.168.2.15/upload"
    print(url)
    # Open the video capture
            # Read a frame from the video capture
        # Convert the frame to JPEG format
    _, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()

    try:
        # Send the frame to the server
        response = requests.post(url, data=frame_bytes, headers={'Content-Type': 'image/jpeg'})
        response.raise_for_status()
        print("Frame sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send frame: {e}")


def post_video_stream_test(url, video_device=0):
    # Open the video capture
    cap = cv2.VideoCapture(video_device)

    try:
        while True:
            # Read a frame from the video capture
            ret, frame = cap.read()

            if not ret:
                break

            # Convert the frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            try:
                # Send the frame to the server
                response = requests.post(url, data=frame_bytes, headers={'Content-Type': 'image/jpeg'})
                response.raise_for_status()
                print("Frame sent successfully!")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send frame: {e}")

    finally:
        # Release the video capture
        cap.release()

# Example usage
video_url = "http://192.168.2.15/upload"  # Replace with the actual server URL
#post_video_stream_test(video_url)

# Example usage
 # Replace with the actual server URL
#post_video_stream(video_url)

def video_stream_socket():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((sys.argv[1], int(sys.argv[2])))
    client_socket.connect(('192.168.2.15', 8000))  # ADD IP HERE
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            print("starting Camera...........")
            time.sleep(2)
            stream = io.BytesIO()        
            for foo in camera.capture_continuous(stream, 'jpeg'):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                stream.seek(0)
                stream.truncate()
    finally:
        connection.close()
        client_socket.close()

def video_stream_socket_1(camera):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #client_socket.connect((sys.argv[1], int(sys.argv[2])))
    client_socket.connect(('192.168.2.15', 8000))  # ADD IP HERE
    connection = client_socket.makefile('wb')
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            print("starting Camera...........")
            time.sleep(2)
            stream = io.BytesIO()        
            for foo in camera.capture_continuous(stream, 'jpeg'):
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                stream.seek(0)
                stream.truncate()
    finally:
        connection.close()
        client_socket.close()
        
#video_stream_socket()
#post_video_stream_test(video_url)