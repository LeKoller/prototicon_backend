from django.urls import path

from .message_consumer import MessageConsumer


websocket_urlpatterns = [
    path('ws/messages/', MessageConsumer.as_asgi())
]
