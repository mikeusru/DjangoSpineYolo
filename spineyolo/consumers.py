from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
import json


class AnalysisConsumer(AsyncJsonWebsocketConsumer):
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

    async def receive_json(self, content):
        json_type = content.get("type", None)
        print("content: ", content)
        print("msg_type: {}".format(json_type))
        # try:
        if json_type == "analysis_message":
            await self.send_message(content['message'])
        elif json_type == "progress":
            await self.send_progress(content['progress'])
        # except ClientError as e:
        #     await self.send_json({"error":, e.code})

    async def send_progress(self, progress):

        await self.channel_layer.group_send(
            self.pk_group_name,
            {
                'type': 'progress_percent',
                'progress': progress
            }
        )

    async def send_message(self, message):

        await self.channel_layer.group_send(
            self.pk_group_name,
            {
                'type': 'analysis_message',
                'message': message
            }
        )
        
    async def progress_percent(self, event):
        progress = event['progress']
        # send progress to websocket
        await self.send_json({
            'progress': progress
        })

    # receive message from pk group
    async def analysis_message(self, event):
        message = event['message']

        # send message to websocket
        await self.send_json({
            'message': message
        })

