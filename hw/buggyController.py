import RPi.GPIO as GPIO 
import py_qmc5883l
import serial
import pynmea2

import time
 

class BuggyController(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BuggyController, cls).__new__(cls)
        return cls.instance
    
    def setDestination(self,lat,long):
        self.destination = (lat,long)
        
    def getDestination(self):
        return self.destination
        

    def magnetoSetup(self):
        self.sensor = py_qmc5883l.QMC5883L()
        self.sensor.calibration = [[1.0270995979508475, -0.020248684731951426, 1902.8581272409879], [-0.020248684731951454, 1.0151297164672932, -2031.7481674046921], [0.0, 0.0, 1.0]]

    def setup(self,in1,in2,en,in3,in4,enb):
        if not hasattr(self,'runSetup'):
            self.runSetup = False
            try:
                self.cleanup()
            except:
                print("cleaned")
            
            self.destination = None
            
            
            
            try:
                self.sensor = py_qmc5883l.QMC5883L()
                self.sensor.calibration = [[1.0270995979508475, -0.020248684731951426, 1902.8581272409879], [-0.020248684731951454, 1.0151297164672932, -2031.7481674046921], [0.0, 0.0, 1.0]]
            except:
                print("magneto setup error")
            self.in1 = in1
            self.in2 = in2
            self.en = en
            self.in3 = in3
            self.in4 = in4
            self.enb = enb

            GPIO.setmode(GPIO.BCM)
            GPIO.setup(in1,GPIO.OUT)
            GPIO.setup(in2,GPIO.OUT)
            GPIO.setup(en,GPIO.OUT)
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.LOW)
            self.p=GPIO.PWM(en,1000)

            GPIO.setup(in3,GPIO.OUT)
            GPIO.setup(in4,GPIO.OUT)
            GPIO.setup(enb,GPIO.OUT)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.LOW)
            self.q=GPIO.PWM(enb,1000)
            self.q.start(30)
            self.p.start(30)
            self.dc = 30

    
    
    def forward(self):
        print("f")
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
    
    def backward(self):
        print("b")
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)
        
    
    def setSpeed(self,s):
        print("set: ",s)
        self.dc = s
        self.p.ChangeDutyCycle(s)
        self.q.ChangeDutyCycle(s)
    

    
    # def left(self):
    #     print("l")
    #     self.p.ChangeDutyCycle(0)
    #     self.q.ChangeDutyCycle(50)

    def left(self):
        print("l")
        # self.p.ChangeDutyCycle(45)
        # self.q.ChangeDutyCycle(45)
        GPIO.output(self.in1,GPIO.HIGH)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.HIGH)
    
    def right(self):
        print("r")
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.HIGH)
        GPIO.output(self.in3,GPIO.HIGH)
        GPIO.output(self.in4,GPIO.LOW)

        
    def mark(self):
        print("marked")
        
    def pick(self):
        print("picked")
    
    def drop(self):
        print("dropped")
        
    def stop(self):
        
        print("s");
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        GPIO.output(self.in3,GPIO.LOW)
        GPIO.output(self.in4,GPIO.LOW)
     
    def gpsSetup(self,port="/dev/ttyS0",baud = 9600,timeout=0.5):
        if not hasattr(self,'gpsSerial'):
            self.gpsSerial=serial.Serial(port=port,baudrate=baud,timeout=timeout)
            dataout = pynmea2.NMEAStreamReader()
        
    def getLatLong(self):
        while True:
            newdata=self.gpsSerial.readline()
            newdata = newdata.decode()
            if newdata[0:6] == "$GPGLL":
                newmsg=pynmea2.parse(newdata)
                lat=newmsg.latitude
                lng=newmsg.longitude
                return (lat,lng)
                
    

    
    def getSmokeLevel(self):
        return 1.234
    
    def get_current_direction(self):
       
        heading = ""
        # while True:
        m = self.sensor.get_magnet()
        x=m[0]
        y=m[1]
        # print(x,y)
        # heading = ""
        if(x<80 and x>-700 and y>=1700 and y<=2150):
            heading = "North"
        elif(x>-1700 and x<-700 and  y>480 and y<1800):
            heading = "North-East"
        elif(x<-1600 and x>-2000 and y<500 and y>-600):
            heading = "East"
        elif(x>-1600 and x<-300 and  y>-1800 and y<400):
            heading = "South-East"
        elif(x>-300 and x<700 and y>-1800 and y<-1400):
            heading = "South"
        elif(x>690 and x<1800 and y<270 and y>-1700):
            heading = "South-West"
        elif(x<1850 and x>1550 and y>=-50 and y<=790):
            heading = "West"
        elif(x>110 and x<1550 and y>790 and y<2000):
            heading = "North-West"
        else:
            heading = "Need Calibration!"

        # print("x = "+str(x)+" y= "+str(y)+" heading = "+heading)
        return heading
        
    def ultrasonicSetup(self,trig,ech):
        if not hasattr(self,'trigger'):
            self.trigger = trig
            self.echo = ech
            
            try:
                self.cleanup()
            except:
                pass

            GPIO.setmode(GPIO.BCM)
            # self.setup()
            GPIO.setup(trig, GPIO.OUT)
            GPIO.setup(ech, GPIO.IN)    
        
    def getDistance(self):      # return distance in cm
        # set Trigger to HIGH
        GPIO.output(self.trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(self.echo) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(self.echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
    
    def cleanup(self):
        print("c")
        GPIO.cleanup()
        
    # def __del__(self):
    #     self.cleanup()
