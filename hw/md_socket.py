import socket
import threading
import time
import numpy as np
from buggyController import BuggyConntroller


port = 23000
ip = "192.168.174.214"
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


buggyController = BuggyConntroller()
buggyController.setup(in1,in2,en,in3,in4,enb)


start_time = -1
stop_thread = False

def timeout(sec):
    while(time.time()-start_time<sec):
        pass
    global prev_cmd
    prev_cmd = 10
    buggyController.stop()


def connect():
    global sock
    try:
        sock.connect((ip,port))
        return 1
    except:
        # print("unable to connect")
        return 0

def setup():
    global sock
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while(not connect()):
        time.sleep(1)
    print("connected to server")

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
            print("zero len")
            sock.close()
            setup()
            cmd = sock.recv(1024).decode()
            
        
        start_time = time.time()
        if(not to.is_alive()):
            to = threading.Thread(target=timeout,args=(2,))
            to.start()
        
        
        print(cmd)
        cmds = cmd.split('\n')[:-1]
        for command in cmds:
            is_forward, speed, sign = command.split(",")
            
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
                buggyController.stop()
                prev_cmd=10
                continue

            cmd = int(cmd)
            if(cmd==0):
                buggyController.setSpeed(speed)
                if prev_cmd == 10:
                    if is_forward:
                        buggyController.forward()
                    else:
                        buggyController.backward()
            
            if(cmd!=prev_cmd and cmd>=1 and cmd<len(cmd_list)):
                prev_cmd = cmd
                cmd = cmd_list[cmd]     #['Start','NULL','Left','Right','Mark','Pick','Drop']
                
                if cmd=="Left":
                    buggyController.left()
                elif cmd=="Right":
                    buggyController.right()
                elif cmd=="Mark":
                    buggyController.mark()
                elif cmd=="Pick":
                    buggyController.pick()
                elif cmd=="Drop":
                    buggyController.drop()
        
else:
    print("The default speed & direction of motor is LOW & Forward.....")
    print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
    print("\n") 

    while(1):

        x=input()
        
        if x=='r':
            print("run")
            if(temp1==1):
                buggyController.forward()
                print("forward")
                x='z'
            else:
                buggyController.backward()
                print("backward")
                x='z'


        elif x=='s':
            print("stop")
            buggyController.stop()
            x='z'

        elif x=='f':
            print("forward")
            buggyController.forward()
            temp1=1
            x='z'

        elif x=='b':
            print("backward")
            buggyController.backward()
            temp1=0
            x='z'

        elif x=='l':
            print("low")
            # speed(x)
            buggyController.setSpeed(50)
            x='z'

        elif x=='m':
            print("medium")
            buggyController.setSpeed(60)
            # speed(x)
            x='z'

        elif x=='h':
            print("high")
            buggyController.setSpeed(70)
            # speed(x)
            x='z'
        
        
        elif x=='e':
            buggyController.cleanup()
            print("GPIO Clean up")
            break
        
        else:
            print("<<<  wrong data  >>>")
            print("please enter the defined data to continue.....")

            
