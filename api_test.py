# importing the requests library
import requests
 
# defining the api-endpoint
API_ENDPOINT = "http://localhost:8000/api/get-buggy-coordinates/"
smoke_ep = 'http://localhost:8000/api/get-smoke-level/'
 

# data to be sent to api
data = {'latitude':1234.2134,
        'longitude': 132414.1234234}
smokeData = {'smokeLevel':12.2}
# sending post request and saving response as response object
r = requests.post(url=API_ENDPOINT, data=data)
r2 = requests.post(url=smoke_ep,data=smokeData)
 
# extracting response text
print(r)