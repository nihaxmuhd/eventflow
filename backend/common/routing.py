
from django.urls import path

from common.consumers import EventFlowConsumer

websocket_urlpatterns = [
    path("ws/events/", EventFlowConsumer.as_asgi()),
]
