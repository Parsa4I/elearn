from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .models import Course


class IsTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)


class IsCourseOwnerMixin:
    def dispatch(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        course = get_object_or_404(Course, slug=slug)
        if request.user != course.teacher:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)
