from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from django.urls import path
from Backend.servers.channel_consumer import EventConsumer, TerminalConsumer


websocket_urlpatterns = [
   path("real-time-notification/<str:user_id>/", EventConsumer),
   path("terminal-access/<str:user_id>/<str:server_id>", TerminalConsumer),
]

application = ProtocolTypeRouter({
'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    )
})

