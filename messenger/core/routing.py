from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/channel/(?P<room_name>\w+)/$", consumers.ChannelConsumer.as_asgi()),
    re_path(r"ws/dialog/(?P<room_name>\w+)/$", consumers.DialogConsumer.as_asgi()),
]
