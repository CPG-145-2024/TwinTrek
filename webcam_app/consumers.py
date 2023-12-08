# yourapp/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CoordinatesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def update_coordinates(self, event):
        latitude = event['latitude']
        longitude = event['longitude']

        # Send latitude and longitude to the client
        await self.send(text_data=json.dumps({
            'latitude': latitude,
            'longitude': longitude,
        }))
