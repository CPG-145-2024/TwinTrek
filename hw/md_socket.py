import RPi.GPIO as GPIO          
from time import sleep
import socket
import threading
import time


port = 23000
ip = "192.168.216.242"
use_socket = True

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
    print("s");
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)


def speed(s):
    if s=='l':
        print("low")
        p.ChangeDutyCycle(40)
        q.ChangeDutyCycle(40)
        

    elif s=='m':
        print("medium")
        p.ChangeDutyCycle(60)
        q.ChangeDutyCycle(60)
        

    elif s=='h':
        print("high")
        p.ChangeDutyCycle(75)
        q.ChangeDutyCycle(75)
        
def cleanup():
    print("c")
    GPIO.cleanup()


if(use_socket):
    cmd_list = ["start","stop","left","right"]

    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip,port))

    prev_cmd = -1
    cmd = -2

    to = threading.Thread(target=timeout,args=(2,))

    while True:
        cmd = sock.recv(4).decode()
        
        start_time = time.time()
        if(not to.is_alive()):
            to = threading.Thread(target=timeout,args=(2,))
            to.start()
        
        
        if(len(cmd)==0):
            cleanup()
            break

        cmd = int(cmd)
        if(cmd!=prev_cmd and cmd>=0 and cmd<len(cmd_list)):
            prev_cmd = cmd
            cmd = cmd_list[cmd]
            if(cmd=="start"):
                forward()
            elif cmd=="stop":
                stop()
            elif cmd=="left":
                left()
            elif cmd=="right":
                right()
        
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

            
