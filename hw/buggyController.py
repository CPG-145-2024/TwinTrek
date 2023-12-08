# import RPi.GPIO as GPIO  

class BuggyConntroller(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(BuggyConntroller, cls).__new__(cls)
        return cls.instance

    def setup(self,in1,in2,en,in3,in4,enb):
        if not hasattr(self,'runSetup'):
            self.runSetup = False
            
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
