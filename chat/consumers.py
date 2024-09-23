from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["course_slug"]
        self.room_group_name = f"chat_{self.room_name}"
        self.user = self.scope["user"]
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": str(self.user),
                "datetime": timezone.now().isoformat(),
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(json.dumps(event))
