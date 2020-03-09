from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.pk = self.scope['url_route']['kwargs']['pk']
        self.pk_group_name = "analysis_%s" % self.pk

        # Join room group
        await self.channel_layer.group_add(
            self.pk_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.pk_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.pk_group_name,
            {
                'type': 'analysis_message',
                'message': message
            }
        )

    # receive message from pk group
    async def analysis_message(self, event):
        message = event['message']

        # send message to websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
