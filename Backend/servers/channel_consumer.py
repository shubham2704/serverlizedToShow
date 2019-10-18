from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
import json, paramiko
from .models import list as server_list



class TerminalConsumer(JsonWebsocketConsumer):

    connected = "";
    
    def connect(self):
        
        self.group_name = self.scope["url_route"]["kwargs"]["user_id"]
        self.server_id = self.scope["url_route"]["kwargs"]["server_id"]

        async_to_sync(self.channel_layer.group_add)(
            self.group_name + self.server_id,
            self.channel_name
        )

        self.accept()

        try:
            get_server = server_list.objects.get(id = int(self.server_id))
            
            os_id = get_server.distribution_id
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.load_system_host_keys()
            self.client.connect(get_server.server_ip, username=get_server.superuser, password=get_server.password)
            print("Connected")
            
            content = {
                'status':'success',
                'msg':'Successfully Connected with root@' + get_server.server_ip + ""
            }
            self.send_json(content)
        except:
            content = {
                'status':'error',
                'msg':'Connection to root@' + get_server.server_ip + " is failed! Try again with refreshing page."
            }
            self.send_json(content)
            

        

    def disconnect(self, close_code):
        print("Closed websocket with code: ", close_code)
        if self.client:
            self.client.close()
        async_to_sync(self.channel_layer.group_discard)(
            'sever_updates',
            self.channel_name
        )
        self.close()



    def receive_json(self, content, **kwargs):
        #json_ld = json.loads(content);
        if content['type'] == "command":
            stdidn,stddout,stdderr=self.client.exec_command(content['command'])
            response = []
            
            for line in stddout.readlines():
                response.append(str(line))


            for lin in stdderr:
                response.append(str(lin))
        print(response)
        self.send_json(response)

        print("Received event: {}".format(content))
        
    

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