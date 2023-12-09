import math
import time
from buggyController  import BuggyController

bc = BuggyController()
bc.gpsSetup()
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

bc.ultrasonicSetup(GPIO_TRIGGER,GPIO_TRIGGER) 




def navigate(End_c):
    
    Ending_Coordinate = [math.radians(End_c[0]), math.radians(End_c[1])]
    direction_to_move = None
    
    while True:
        
        if(direction_to_move == None or direction_to_move!=bc.get_current_direction()):
            Start_c = bc.getLatLong()
            Starting_Coordinate =[ math.radians(Start_c[0]), math.radians(Start_c[1])]
            

            X =  math.cos(Ending_Coordinate[0]) * math.sin(Ending_Coordinate[1]-Starting_Coordinate[1])

            Y = math.cos(Starting_Coordinate[0]) * math.sin(Ending_Coordinate[0]) - math.sin(Starting_Coordinate[0]) * math.cos(Ending_Coordinate[0]) * math.cos(Ending_Coordinate[1]-Starting_Coordinate[1])

            B = math.atan2(X,Y)
            
            B_degrees = math.degrees(B)
            print(B_degrees)

            direction_to_move = ""

            if(B_degrees<=15 and B_degrees>=-15):
                direction_to_move="North"
            elif(B_degrees>15 and B_degrees<75):
                direction_to_move="North-East"
            elif(B_degrees>=75 and B_degrees<=105):
                direction_to_move="East"
            elif(B_degrees>105 and B_degrees<165):
                direction_to_move="South-East"
            elif(B_degrees>=165 or B_degrees<=-165):
                direction_to_move="South"
            elif(B_degrees>-165 and B_degrees<-105):
                direction_to_move="South-West"
            elif(B_degrees>=-105 and B_degrees<=-75):
                direction_to_move="West"
            elif(B_degrees<-15 and B_degrees>-75):
                direction_to_move="North-West"
            print("Move "+direction_to_move)

        #get current direection from magnetometer
        while(bc.get_current_direction()!=direction_to_move):
            #rotate till current direction!= direction_to_move
            bc.right()
        
        
        #keep moving till no obstacle encounter
        while(bc.getDistance()>20):
            bc.forward()
            if(bc.getLatLong()==End_c):
                return

        
        if(bc.getDistance()<=20):
            print("Stop")
            # rotate buggy right while ultrasonic.distance<0.2
            while(bc.getDistance()<=20):
                bc.right()
            # move buggy in that direction for 5 seconds
            bc.forward()
            time.sleep(5)

End_c = bc.getDestination()
while End_c==None:
    time.sleep(1)
    End_c = bc.getDestination()

navigate(End_c)