from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/spineyolo/images/analyze_image(?P<pk>\w+)/$', consumers.ChatConsumer),
]