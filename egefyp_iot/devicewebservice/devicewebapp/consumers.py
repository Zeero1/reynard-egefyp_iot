import json
# from channels.generic.websocket import WebsocketConsumer  
from channels.generic.websocket import AsyncWebsocketConsumer  
from random import randint
# from time import sleep  
from asyncio import sleep

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        for i in range(1000):
            await self.send(json.dumps({'value': randint(0, 100)}))
            await sleep(1)
