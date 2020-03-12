from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from spineyolo.models import toggle_rating


class RatingConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.group_name = "rating"
        # Join room group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        json_type = content.get("type", None)
        # try:
        if json_type == "rating_toggle":
            await self.send_rating(content['pk'])

    async def send_rating(self, pk):
        rating = await self.change_rating_in_database(pk)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'rating_toggle',
                'rating': rating,
                'pk': pk
            }
        )

    # message handler
    async def rating_toggle(self, event):
        rating = event['rating']
        pk = event['pk']
        # send message to websocket
        await self.send_json({
            'rating': rating,
            'pk': pk
        })

    @database_sync_to_async
    def change_rating_in_database(self, pk):
        return toggle_rating(pk)



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
        elif json_type == "progress_percent":
            await self.send_progress(content['progress'])
        elif json_type == "finished":
            await self.send_progress(content['finished'])
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

    async def send_finished(self, message):

        await self.channel_layer.group_send(
            self.pk_group_name,
            {
                'type': 'finished_message',
                'finished': message
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

    # receive message from pk group
    async def finished_message(self, event):
        message = event['finished']
        spine_coordinates_url = event['spine_coordinates_url']
        analyzed_image_url = event['analyzed_image_url']

        # send message to websocket
        await self.send_json({
            'finished': message,
            'spine_coordinates_url': spine_coordinates_url,
            'analyzed_image_url': analyzed_image_url
        })
