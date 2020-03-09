from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


class FrontEndUpdater:

    def __init__(self, pk):
        self.pk = pk

    def update_progress(self, progress_percentage):
        # message = "progress is at {}%!".format(progress_percentage)
        self.__send_progress(progress_percentage)

    def post_message(self, message):
        self.__send_a_message(message)

    def analysis_done(self):
        self.update_progress(100)
        self.__send_a_message("Analysis Done")

    def __send_a_message(self, message):
        pk_group_name = "analysis_%s" % self.pk
        async_to_sync(channel_layer.group_send)(
            pk_group_name,
            {
                'type': 'analysis_message',
                'message': message
            })

    def __send_progress(self, progress):
        pk_group_name = "analysis_%s" % self.pk
        async_to_sync(channel_layer.group_send)(
            pk_group_name,
            {
                'type': 'progress_percent',
                'progress': progress
            })
