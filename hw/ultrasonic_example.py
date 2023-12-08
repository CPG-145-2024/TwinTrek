#Libraries
from buggyController  import BuggyConntroller
import time

bc = BuggyConntroller()
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

bc.ultrasonicSetup(GPIO_TRIGGER,GPIO_TRIGGER) 

    
 
if __name__ == '__main__':
    try:
        while True:
            dist = bc.getDistance()
            print ("Measured Distance = %.1f cm" % dist)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        