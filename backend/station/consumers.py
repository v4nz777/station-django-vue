
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


def add_activities_db(data):
    from .models import Activity
    from .serializers import ActivitySerializer
    
    activity = Activity()
    activity.new_activity(data["user"],data["subject"])
    serializer = ActivitySerializer(activity)
    return serializer.data

class ActivityConsumer(WebsocketConsumer):
    def connect(self):
        self.room = 'activities'
        async_to_sync(self.channel_layer.group_add)(
            self.room,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        data = add_activities_db(text_data_json) #add to DB and get serialized result
        async_to_sync(self.channel_layer.group_send)(
            self.room,
            {
                'type': 'activity_message', # Name of the function for this connection
                'message': data
            }
        )
    
    def activity_message(self,event): # Here is the function that was named above
        message = event['message']
        self.send(text_data=json.dumps({
            'type': 'activity',
            'message': message
        }))
