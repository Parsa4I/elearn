from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.conf import settings
from django.core import validators


class Star(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stars"
    )
    points = models.PositiveSmallIntegerField(
        validators=[validators.MaxValueValidator(5)]
    )

    class Meta:
        indexes = [models.Index(fields=["content_type", "object_id"])]
        unique_together = [("object_id", "content_type", "user")]

    def __str__(self):
        return f"{self.user} rated {self.content_object}: {self.points}"
