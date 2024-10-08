from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.utils import timezone
from .models import ChatMessage
from courses.models import Course
from django.core.cache import cache


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

        course = await Course.objects.aget(slug=self.room_name)
        await ChatMessage.objects.acreate(user=self.user, course=course, body=message)
        await cache.adelete_many([f"messages_{self.room_name}"])
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
        event["message"]
        await self.send(json.dumps(event))
