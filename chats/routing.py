# chats/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # This must match the URL in your JavaScript
    re_path(r'ws/chat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
]