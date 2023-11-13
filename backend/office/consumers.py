import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync



def get_latest_ad(data):
    from .models import Ad
    from .serializers import AdSerializer

    latest = Ad.objects.get(id=int(data["item"]))
    return AdSerializer(latest).data

class AdConsumer(WebsocketConsumer):
    def connect(self):
        self.room = 'ads'
        async_to_sync(self.channel_layer.group_add)(
            self.room,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        data = get_latest_ad(text_data_json) #add to DB and get serialized result
        async_to_sync(self.channel_layer.group_send)(
            self.room,
            {
                'type': 'ads_message', # Name of the function for this connection
                'message': data,
                'author': text_data_json["author"]
            }
        )
    
    def ads_message(self,event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'ads',
            'message': message,
            'author':event['author']
        }))

