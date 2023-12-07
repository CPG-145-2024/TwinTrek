import math
import time
# from gpiozero  import DistanceSensor
# ultrasonic = DistanceSensor(echo=17, trigger=4)
# ultrasonic.threshold_distance = 0.2 # in meters


Starting_Coordinate =[ math.radians(0), math.radians(0)]
Ending_Coordinate = [math.radians(-20), math.radians(20)]

# X =  math.cos(Ending_Coordinate[0]) * math.sin(Ending_Coordinate[1]-Starting_Coordinate[1])

# Y = math.cos(Starting_Coordinate[0]) * math.sin(Ending_Coordinate[0]) - math.sin(Starting_Coordinate[0]) * math.cos(Ending_Coordinate[0]) * math.cos(Ending_Coordinate[1]-Starting_Coordinate[1])

# B = math.atan2(X,Y)
# # print(math.cos(Starting_Coordinate[0]),math.sin(Ending_Coordinate[0]))
# # print(X,Y,B)
# B_degrees = math.degrees(B)

while True:

    X =  math.cos(Ending_Coordinate[0]) * math.sin(Ending_Coordinate[1]-Starting_Coordinate[1])

    Y = math.cos(Starting_Coordinate[0]) * math.sin(Ending_Coordinate[0]) - math.sin(Starting_Coordinate[0]) * math.cos(Ending_Coordinate[0]) * math.cos(Ending_Coordinate[1]-Starting_Coordinate[1])

    B = math.atan2(X,Y)
    # print(math.cos(Starting_Coordinate[0]),math.sin(Ending_Coordinate[0]))
    # print(X,Y,B)
    B_degrees = math.degrees(B)
    # ultrasonic.wait_for_in_range()
    # if(ultrasonic.distance<0.2):
    #     print("Stop")
    #     # some module to navigate
    #     continue


    # ultrasonic.wait_for_out_of_range()
    # print("Out of range")


    print(B_degrees)

    if(B_degrees<=15 and B_degrees>=-15):
        print("Move North")
    elif(B_degrees>15 and B_degrees<75):
        print("Move North-East")
    elif(B_degrees>=75 and B_degrees<=105):
        print("Move East")
    elif(B_degrees>105 and B_degrees<165):
        print("Move South-East")
    elif(B_degrees>=165 or B_degrees<=-165):
        print("Move South")
    elif(B_degrees>-165 and B_degrees<-105):
        print("Move South-West")
    elif(B_degrees>=-105 and B_degrees<=-75):
        print("Move West")
    elif(B_degrees<-15 and B_degrees>-75):
        print("Move North-West")
    time.sleep(2)