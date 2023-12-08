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
import time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json


# Global variables
detector = HandDetector() #detector obj

forward = False # is going forward or backward
speed = 0   # speed of buggy

labels = ['Start','NULL','Left','Right','Mark','Pick','Drop']   # labels of gestures

kpc = KeyPointClassifier()  # gesture classification object

latitude = 30.352899
longitude = 76.386324

# socket setup
server_port = 23000
sock = None
use_socket = True

@api_view(['GET'])
def get_coordinates(request):
    global latitude, longitude

    # Your logic to update latitude and longitude (replace with your implementation)
    # For example, you might update these values from a sensor or database
    latitude += 0.1
    longitude += 0.2

    data = {
        'latitude': latitude,
        'longitude': longitude,
    }
    return Response(data)

@csrf_exempt
@require_POST
def post_coordinates(request):
    try:
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Update global variables with new coordinates
        global global_latitude, global_longitude
        global_latitude = latitude
        global_longitude = longitude

        print("Received coordinates - Latitude:", latitude, "Longitude:", longitude)

        return JsonResponse({'message': 'Coordinates updated successfully.'})
    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@api_view(['POST'])    
def getBuggyPosition(request):
    try:
        data = request.data
        global latitude, longitude
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        
        print(latitude,longitude)
        return JsonResponse({'status' : 'success'})
    except:
        return JsonResponse({'status': 'error'})


@api_view(['POST'])    
def getSmokeLevel(request):
    try:
        data = request.data
        global smokeLevel
        smokeLevel = float(data.get('smokeLevel'))        
        print(smokeLevel)
        return JsonResponse({'status' : 'success'})
    except:
        return JsonResponse({'status': 'error'})

def send_cmd(cmd):
    global sock
    try:
        sock.send(cmd.encode())
    except:
        print("Connection with buggy lost")
        if(sock is not None):
            sock.close()

    return


def socket_setup(): 
    global sock
    # print("here")
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
            
            message = str(forward) + "," + str(speed) + "," + str(signId) + '\n'
            send_cmd(message)
            # print(labels[signId])
            # if(signId==0):
            #     print(forward,speed)
