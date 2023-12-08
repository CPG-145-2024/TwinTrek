import requests
from buggyController import BuggyConntroller
import time
 
position_endpoint = "http://localhost:8000/api/get-buggy-coordinates/"
smoke_endpoint = 'http://localhost:8000/api/get-smoke-level/'
 
 
bc = BuggyConntroller()

while True:
    lat,long = bc.getLatLong()
    smokeLevel = bc.getSmokeLevel()


    # data to be sent to api
    posData = {'latitude':lat,
            'longitude': long}
    smokeData = {'smokeLevel':smokeLevel}

    requests.post(url=position_endpoint, data=posData)
    requests.post(url=smoke_endpoint,data=smokeData)
    time.sleep(1)
 
