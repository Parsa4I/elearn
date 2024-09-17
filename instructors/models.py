from django.db import models
from django.conf import settings


class InstructingRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="instruction_requests",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
