from buggyController import BuggyConntroller

bc = BuggyConntroller()
bc.gpsSetup()

while True:
	lat,lng = bc.getLatLong() # return lat,lng tuple
	gps = "Latitude=" + str(lat) + " and Longitude=" + str(lng)
	print(gps)
	