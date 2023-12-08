# import RPi.GPIO as GPIO 
# import py_qmc5883l

import time
 

class BuggyConntroller(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BuggyConntroller, cls).__new__(cls)
        return cls.instance

    def setup(self,in1,in2,en,in3,in4,enb):
        if not hasattr(self,'runSetup'):
            self.runSetup = False

            # self.sensor = py_qmc5883l.QMC5883L()
            # self.sensor.calibration = [[1.0270995979508475, -0.020248684731951426, 1902.8581272409879], [-0.020248684731951454, 1.0151297164672932, -2031.7481674046921], [0.0, 0.0, 1.0]]
            
            # GPIO.setmode(GPIO.BCM)
            # GPIO.setup(in1,GPIO.OUT)
            # GPIO.setup(in2,GPIO.OUT)
            # GPIO.setup(en,GPIO.OUT)
            # GPIO.output(in1,GPIO.LOW)
            # GPIO.output(in2,GPIO.LOW)
            # self.p=GPIO.PWM(en,1000)

            # GPIO.setup(in3,GPIO.OUT)
            # GPIO.setup(in4,GPIO.OUT)
            # GPIO.setup(enb,GPIO.OUT)
            # GPIO.output(in3,GPIO.LOW)
            # GPIO.output(in4,GPIO.LOW)
            # self.q=GPIO.PWM(enb,1000)
            # self.q.start(25)
            # self.p.start(25)
            
    def forward(self):
        print("f")
        # GPIO.output(in1,GPIO.HIGH)
        # GPIO.output(in2,GPIO.LOW)
        # GPIO.output(in3,GPIO.HIGH)
        # GPIO.output(in4,GPIO.LOW)
    
    def backward(self):
        print("b")
        # GPIO.output(in1,GPIO.LOW)
        # GPIO.output(in2,GPIO.HIGH)
        # GPIO.output(in3,GPIO.LOW)
        # GPIO.output(in4,GPIO.HIGH)
    
    def setSpeed(self,s):
        print("set: ",s)
        # self.p.ChangeDutyCycle(s)
        # self.q.ChangeDutyCycle(s)
    
    def cleanup(self):
        print("c")
        # GPIO.cleanup()
    
    def left(self):
        print("l")
        

    def right(self):
        print("r")
        
    def mark(self):
        print("marked")
        
    def pick(self):
        print("picked")
    
    def drop(self):
        print("dropped")
        
    def stop(self):
        
        print("s");
        # GPIO.output(in1,GPIO.LOW)
        # GPIO.output(in2,GPIO.LOW)
        # GPIO.output(in3,GPIO.LOW)
        # GPIO.output(in4,GPIO.LOW)
    def getLatLong(self):
        return (30.7,64.1)
    
    def getSmokeLevel(self):
        return 1.234
    
    def get_current_direction(self):
       
        heading = ""
        # # while True:
        # m = self.sensor.get_magnet()
        # x=m[0]
        # y=m[1]
        # # heading = ""
        # if(x<80 and x>-700 and y>=1700 and y<=2150):
        #     heading = "North";
        # elif(x>-1700 and x<-700 and  y>480 and y<1800):
        #     heading = "North-East";
        # elif(x<-1600 and x>-2000 and y<500 and y>-600):
        #     heading = "East";
        # elif(x>-1600 and x<-300 and  y>-1800 and y<400):
        #     heading = "South-East";
        # elif(x>-300 and x<700 and y>-1800 and y<-1400):
        #     heading = "South";
        # elif(x>690 and x<1800 and y<270 and y>-1700):
        #     heading = "South-West";
        # elif(x<1850 and x>1550 and y>=-50 and y<=790):
        #     heading = "West";
        # elif(x>110 and x<1550 and y>790 and y<2000):
        #     heading = "North-West";

        # # print("x = "+str(x)+" y= "+str(y)+" heading = "+heading)
        # return heading
        
    
