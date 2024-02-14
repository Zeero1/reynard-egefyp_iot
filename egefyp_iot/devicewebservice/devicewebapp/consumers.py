import json
import asyncio
import traceback
from channels.generic.websocket import AsyncWebsocketConsumer  
from .views import *

class GraphConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def send_message(self, message_data):
        await self.send(json.dumps(message_data))

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({'error': error_message}))

    async def disconnect(self):
        pass