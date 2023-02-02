from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"sockets/activities", consumers.ActivityConsumer.as_asgi())
]