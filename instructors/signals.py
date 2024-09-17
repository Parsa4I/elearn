from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import InstructingRequest


@receiver(post_save, sender=InstructingRequest)
def instructor_request_approved_handler(sender, instance, **kwargs):
    if instance.approved:
        user = instance.user
        user.is_instructor = True
        user.save()
