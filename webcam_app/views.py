from rest_framework.decorators import api_view
from rest_framework.response import Response

import cv2
import numpy as np
import threading

import numpy as np

from .gestureDetector import HandDetector
from .gestureDetector import KeyPointClassifier

import socket

from django.http.response import StreamingHttpResponse
from webcam_app.camera import BuggyCam

# Global variables
detector = HandDetector() #detector obj

forward = False # is going forward or backward
speed = 0   # speed of buggy

labels = ['Start','NULL','Left','Right','Mark','Pick','Drop']   #labels of gestures

kpc = KeyPointClassifier()  #gesture classification object


# socket setup
server_port = 23000
sock = None
use_socket = True

def send_cmd(cmd):
    global sock
    try:
        sock.send(cmd.encode())
    except:
        print("Connection with buggy lost")
        sock.close()

    return


def socket_setup(): 
    global sock
    print("here")
    listen_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    listen_sock.bind(("0.0.0.0",server_port))
    listen_sock.listen(10)
    while True:
        (comm,addr) = listen_sock.accept()
        sock = comm
    

def setup():
    
    if use_socket:
        threading.Thread(target=socket_setup).start()

setup()




@api_view(['POST'])
def webcam_image_view(request):
    
    if request.method == 'POST':
        
        data = np.asarray(bytearray(request.FILES['image'].read()),dtype='uint8')
        data = cv2.imdecode(data,cv2.IMREAD_COLOR)
        
        processHand(data)
            
    return Response({'message': 'Webcam image processed successfully'})

def gen(camera):
	while True:
		frame = camera.get_frame()
		yield (b'--frame\r\n'
				b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def buggy_feed(request):
	return StreamingHttpResponse(gen(BuggyCam()),
					content_type='multipart/x-mixed-replace; boundary=frame')


def processHand(image):
    # img = cv2.flip(image,1)
    global forward
    global speed

    hands_info = detector.getHandInfo(image)

    for hand in hands_info:
        if(hand['hand']=='Left'):
            
            xt,yt = hand['landmarks'][4][0],hand['landmarks'][4][1]
            xf,yf = hand['landmarks'][8][0],hand['landmarks'][8][1]

            forward = yt>yf
            # print(forward)

            xmin,xmax,ymin,ymax = detector.getBoundingValues(hand['landmarks'])

            #scale for speed independence
            xt = np.interp(xt,(xmin,xmax),(0,300))
            xf = np.interp(xf,(xmin,xmax),(0,300))
            yt = np.interp(yt,(ymin,ymax),(0,300))
            yf = np.interp(yf,(ymin,ymax),(0,300))
            
            speed = np.hypot(xt-xf,yt-yf)  # goes atmax to 300
            print(speed)
            # print(preprocessed_lm)
        else:
            preProcessedLandmark = detector.preprocessLandmark(hand['landmarks'])
            signId = kpc(preProcessedLandmark)
            
            message = str(forward) + " " + str(speed) + " " + str(signId)
            send_cmd(message)
            # print(labels[signId])
            # if(signId==0):
            #     print(forward,speed)


