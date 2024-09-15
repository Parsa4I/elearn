from django.contrib import admin
from .models import Course, Subject


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher")
    raw_id_fields = ("students",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["title"]
