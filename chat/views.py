from django.views.generic.base import TemplateResponseMixin
from django.views.generic import View
from courses.models import Course
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from rest_framework.generics import ListAPIView
from .serializers import ChatMessageSerializer
from .models import ChatMessage
from django.shortcuts import get_object_or_404
from django.core.cache import cache


class ChatRoomView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "chat/chat_room.html"

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        if (
            course not in request.user.courses_joined.all()
            and request.user != course.teacher
        ):
            return HttpResponseForbidden()
        return self.render_to_response({"course": course})


class ChatMessageDetailAPIView(ListAPIView):
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        course_slug = self.kwargs["slug"]
        messages = cache.get(f"messages_{course_slug}")

        if not messages:
            course = get_object_or_404(Course, slug=self.kwargs["slug"])
            messages = ChatMessage.objects.filter(course=course)
            cache.set(f"messages_{course_slug}", messages, 10 * 60)

        return messages
