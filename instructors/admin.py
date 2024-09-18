from django.contrib import admin
from .models import InstructingRequest


@admin.register(InstructingRequest)
class InstructorRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "created", "approved")
    list_editable = ["approved"]
