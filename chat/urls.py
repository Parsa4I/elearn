from django.urls import path
from . import views


app_name = "chat"

urlpatterns = [
    path("<slug:slug>/", views.ChatRoomView.as_view(), name="chat_room"),
    path(
        "<slug:slug>/messages/",
        views.ChatMessageDetailAPIView.as_view(),
        name="messages",
    ),
]
