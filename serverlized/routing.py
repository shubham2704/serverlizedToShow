from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.urls import path
from Backend.servers.channel_consumer import EventConsumer


websocket_urlpatterns = [
   path("real-time-notification/<str:user_id>/", EventConsumer),
]

application = ProtocolTypeRouter({
'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

