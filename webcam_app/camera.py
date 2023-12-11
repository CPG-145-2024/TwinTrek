from imutils.video import VideoStream
import imutils
import cv2
import os
import urllib.request
import numpy as np
from django.conf import settings
from socket import *
import time
import numpy as np



class BuggyCam(object):
	def __init__(self):
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind(('0.0.0.0', 22000))
		self.sock.listen(10)

	def __del__(self):
		cv2.destroyAllWindows()
		self.sock.close()

	def get_frame(self):

		
		(comm, addr) = self.sock.accept()
		data=bytes()
		while True:
			rcv = comm.recv(1000000)
			if not rcv: break
			data+=rcv
			
		data = np.asarray(bytearray(data),dtype='uint8')
		return data.tobytes()
		# data = cv2.imdecode(data,cv2.IMREAD_COLOR)
		# print("Received image from buggy")
		# cv2.imshow("From Buggy to Server",data)
		# if cv2.waitKey(1)&0xFF == ord('q'):
		# 	break
		comm.close()