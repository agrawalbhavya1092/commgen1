from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Campaign 

class AutoSaveEditorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connecting websocket.........",)
        await self.accept()

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         self.channel_name
    #     )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['messagess']
        self.room_name = self.scope['url_route']['kwargs']['slug']
        print("receive..............",self.room_name)
        Campaign.objects.filter(slug=self.room_name).update(campaign_body = message)

        # Send message to room group
        await self.send(text_data=json.dumps({"message":message}))
