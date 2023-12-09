import requests
# from buggyController import BuggyConntroller
import time
 
server_ip = "192.168.111.214"

position_endpoint = "http://"+server_ip+":8000/api/get-buggy-coordinates/"
smoke_endpoint = 'http://'+server_ip+':8000/api/get-smoke-level/'
 
 
# bc = BuggyConntroller()

while True:
#     lat,long = bc.getLatLong()
#     smokeLevel = bc.getSmokeLevel()
    lat,long = (213.123,123.234)
    smokeLevel =212.12


    # data to be sent to api
    posData = {'latitude':lat,
            'longitude': long}
    smokeData = {'smokeLevel':smokeLevel}

    requests.post(url=position_endpoint, data=posData)
    requests.post(url=smoke_endpoint,data=smokeData)
    time.sleep(1)
 
