from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all()
            if self.for_fields:
                query_filter = {
                    field: getattr(model_instance, field) for field in self.for_fields
                }
                qs = qs.filter(**query_filter)
                try:
                    last_one = qs.latest(self.attname)
                    value = getattr(last_one, self.attname) + 1
                except ObjectDoesNotExist:
                    value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)


class Subject(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    overview = models.TextField()
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses_created",
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="courses"
    )
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="courses_joined"
    )

    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, related_name="modules", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = OrderField(for_fields=["course"])

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["order"]
        indexes = [models.Index(fields=["order"])]


class Content(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="contents"
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="contents"
    )
    item_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "item_id")
    order = OrderField(for_fields=["module"])

    class Meta:
        ordering = ["order"]
        indexes = [models.Index(fields=["order"])]


class ItemBase(models.Model):
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Text(ItemBase):
    content = models.TextField()


class Image(ItemBase):
    image = models.ImageField(upload_to="media/images")


class Video(ItemBase):
    video = models.FileField(upload_to="media/videos")


class File(ItemBase):
    file = models.FileField(upload_to="media/files")
