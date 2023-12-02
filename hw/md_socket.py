import RPi.GPIO as GPIO          
from time import sleep
import socket
import threading
import time
import numpy as np


port = 23000
ip = "127.0.0.1"
use_socket = True
is_forward = True
speed = 0
sock = None


in1 = 19
in2 = 13
en = 26
temp1=1
in3 = 6
in4 = 5
enb = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.setup(enb,GPIO.OUT)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
q=GPIO.PWM(enb,1000)



q.start(25)
p.start(25)
print("\n")


start_time = -1
stop_thread = False

def timeout(sec):
    while(time.time()-start_time<sec):
        pass
    stop()


def forward():
    print("f")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)

def backward():
    print("b")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)

def left():
    print("l")
    pass

def right():
    print("r")
    pass

def stop():
    global prev_cmd
    prev_cmd = 10
    print("s");
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)


def setSpeed(s):
    print("set: ",s)
    p.ChangeDutyCycle(s)
    q.ChangeDutyCycle(s)
    
        
def cleanup():
    print("c")
    GPIO.cleanup()


def setup():
    global sock
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip,port))

if(use_socket):
    cmd_list = ['Start','NULL','Left','Right','Mark','Pick','Drop']

    setup()

    prev_cmd = -1
    cmd = -2

    to = threading.Thread(target=timeout,args=(2,))

    while True:
        try:
            cmd = sock.recv(1024).decode()
            if(len(cmd)==0):
                sock.close()
                setup()
            cmd = sock.recv(1024).decode()
        except:
            sock.close()
            setup()
            cmd = sock.recv(1024).decode()
            
        while(len(cmd)==0):
            sock.close()
            setup()
            cmd = sock.recv(1024).decode()
            
        
        start_time = time.time()
        if(not to.is_alive()):
            to = threading.Thread(target=timeout,args=(2,))
            to.start()
        
        
        print(cmd)
        is_forward, speed, sign = cmd.split(" ")
        
        if(is_forward[0]=='T'):
            is_forward=True
        else:
            is_forward=False
        
        speed = float(speed)
        cmd = int(sign)
        if(speed < 60):
            speed = 0
        else:
            speed = np.interp(speed,(50,300),(50,100))
            speed = speed//1
        
        if(speed==0 and cmd == 0):
            stop()
            prev_cmd=10
            continue

        cmd = int(cmd)
        if(cmd==0):
            setSpeed(speed)
            if prev_cmd == 10:
                if is_forward:
                    forward()
                else:
                    backward()
        
        if(cmd!=prev_cmd and cmd>=1 and cmd<len(cmd_list)):
            prev_cmd = cmd
            cmd = cmd_list[cmd]     #['Start','NULL','Left','Right','Mark','Pick','Drop']
            
            if cmd=="Left":
                left()
            elif cmd=="Right":
                right()
            elif cmd=="Mark":
                print("Mark")
            elif cmd=="Pick":
                print("Pick")
            elif cmd=="Drop":
                print("Drop")
        
else:
    print("The default speed & direction of motor is LOW & Forward.....")
    print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
    print("\n") 

    while(1):

        x=input()
        
        if x=='r':
            print("run")
            if(temp1==1):
                forward()
                print("forward")
                x='z'
            else:
                backward()
                print("backward")
                x='z'


        elif x=='s':
            print("stop")
            stop()
            x='z'

        elif x=='f':
            print("forward")
            forward()
            temp1=1
            x='z'

        elif x=='b':
            print("backward")
            backward()
            temp1=0
            x='z'

        elif x=='l':
            print("low")
            speed(x)
            x='z'

        elif x=='m':
            print("medium")
            speed(x)
            x='z'

        elif x=='h':
            print("high")
            speed(x)
            x='z'
        
        
        elif x=='e':
            cleanup()
            print("GPIO Clean up")
            break
        
        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")

            
