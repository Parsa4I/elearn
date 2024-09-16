from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def validate_video_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".mp4", ".mkv"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported video file. Only MP4 and MKV is accepted.")


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
        settings.AUTH_USER_MODEL, related_name="courses_joined", blank=True
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


class ItemBase(models.Model):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="%(class)s_items"
    )
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    order = models.PositiveIntegerField(blank=True)

    class Meta:
        abstract = True
        ordering = ["order"]
        indexes = [models.Index(fields=["order"])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs) -> None:
        text_count = self.module.text_items.count()
        image_count = self.module.image_items.count()
        video_count = self.module.video_items.count()
        file_count = self.module.file_items.count()
        total_items = text_count + image_count + video_count + file_count
        self.order = total_items + 1
        return super().save(*args, **kwargs)


class Text(ItemBase):
    content = models.TextField()


class Image(ItemBase):
    image = models.ImageField(upload_to="images/")


class Video(ItemBase):
    video = models.FileField(upload_to="videos/", validators=[validate_video_extension])


class File(ItemBase):
    file = models.FileField(upload_to="files/")
