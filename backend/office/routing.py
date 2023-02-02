from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"sockets/ads", consumers.AdConsumer.as_asgi())
]