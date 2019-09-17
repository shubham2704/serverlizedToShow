from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
import json

class EventConsumer(JsonWebsocketConsumer):
    
    def connect(self):
        
        self.group_name = self.scope["url_route"]["kwargs"]["user_id"]

        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        async_to_sync(self.channel_layer.group_discard)(
            'sever_updates',
            self.channel_name
        )
        self.close()

    def receive_json(self, content, **kwargs):
        print("Received event: {}".format(content))
        self.send_json(content)

    # ------------------------------------------------------------------------------------------------------------------
    # Handler definitions! handlers will accept their corresponding message types. A message with type event.alarm
    # has to have a function event_alarm
    # ------------------------------------------------------------------------------------------------------------------

    def events_alarm(self, event):
        self.send_json(event)