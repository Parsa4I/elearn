from django.db import models
from django.conf import settings
from courses.models import Course


class ChatMessage(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="messages",
        null=True,
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="messages"
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["course", "user"])]
