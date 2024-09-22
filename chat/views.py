from django.views.generic import TemplateView


class ChatRoomView(TemplateView):
    template_name = "chat/chat_room.html"
