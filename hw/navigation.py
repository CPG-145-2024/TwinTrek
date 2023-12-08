import math
import time
# from gpiozero  import DistanceSensor
# from buggyController import BuggyConntroller
# ultrasonic = DistanceSensor(echo=18, trigger=24)
# ultrasonic.threshold_distance = 0.2 # in meters

# bc = BuggyConntroller()
# Start_c=bc.getLatLong()
Start_c=[0,0]
End_c=[0,20]

def navigate(Start_c,End_c):
    # Starting_Coordinate =[ math.radians(Start_c[0]), math.radians(Start_c[1])]
    Ending_Coordinate = [math.radians(End_c[0]), math.radians(End_c[1])]

    while True:
        
        # Start_c = bc.getLatLong()
        Starting_Coordinate =[ math.radians(Start_c[0]), math.radians(Start_c[1])]
        # get latitude and longitude from gps
        print(ultrasonic.distance)
        # ultrasonic.wait_for_in_range()
        # if(ultrasonic.distance<0.2):
            # print("Stop")
        
            # rotate buggy right while ultrasonic.distance<0.2
            # move buggy in that direction for 5 seconds
            # continue


        # ultrasonic.wait_for_out_of_range()
        # print("Out of range")

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
        #bc.get_current_direction()
        #rotate till current direction!= direction_to_move
        #keep moving till no obstacle encounter

        # if(ultrasonic.distance<0.2):
        #     print("Stop")
            # rotate buggy right while ultrasonic.distance<0.2
            # move buggy in that direction for 5 seconds
            # continue
        time.sleep(2)
navigate(Start_c,End_c)