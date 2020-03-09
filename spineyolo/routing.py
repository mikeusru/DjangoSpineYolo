from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/spineyolo/images/analyze/(?P<pk>\w+)/$', consumers.ChatConsumer),
]
