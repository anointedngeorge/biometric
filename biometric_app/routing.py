import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from biometric_app.consumers import VideoConsumer


application = ProtocolTypeRouter({
    'websocket': URLRouter([
        re_path(r'^ws/video/$', VideoConsumer.as_asgi()),
    ]),
})
