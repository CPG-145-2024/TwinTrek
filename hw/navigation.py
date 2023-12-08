import math
import time
from buggyController  import BuggyConntroller

bc = BuggyConntroller()
bc.gpsSetup()
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24

bc.ultrasonicSetup(GPIO_TRIGGER,GPIO_TRIGGER) 




def navigate(End_c):
    
    Ending_Coordinate = [math.radians(End_c[0]), math.radians(End_c[1])]

    while True:
        
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
        curr_direction = bc.get_current_direction()
        #rotate till current direction!= direction_to_move
        #keep moving till no obstacle encounter
        ultra_distance = dist = bc.getDistance()
        if(ultra_distance<20):
            print("Stop")
            # rotate buggy right while ultrasonic.distance<0.2
            # move buggy in that direction for 5 seconds
            # continue
        # time.sleep(2)

End_c = bc.getDestination()

navigate(End_c)