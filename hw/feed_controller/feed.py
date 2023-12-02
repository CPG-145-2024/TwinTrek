import socket
import cv2
import time
import humanDetector


server_ip = "192.168.174.214"
server_port=22000


cam = cv2.VideoCapture(0)
humanDetector = humanDetector.HumanDetector()


while True:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((server_ip,server_port))

    ret ,frame = cam.read()
    
    if(not ret):
        print("unable to capture image")
        continue
    
    frame = humanDetector.drawHuman(frame)
    
    img = cv2.imencode('.jpeg',frame)[1]


    # print("Sent image to server")

    sock.send(img)

    # time.sleep(0.033)       # 30 fps

    sock.close()


