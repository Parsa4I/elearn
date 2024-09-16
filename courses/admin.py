from django.contrib import admin
from .models import Course, Subject, Module, Text, Image, Video, File


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher")
    raw_id_fields = ("students",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ["title"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ["pk", "title"]


class ItemBaseAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "order", "module", "course"]

    def course(self, obj):
        return obj.module.course


@admin.register(Text)
class TextAdmin(ItemBaseAdmin):
    pass


@admin.register(Image)
class ImageAdmin(ItemBaseAdmin):
    pass


@admin.register(Video)
class VideoAdmin(ItemBaseAdmin):
    pass


@admin.register(File)
class FileAdmin(ItemBaseAdmin):
    pass
