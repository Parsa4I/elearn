from django.views.generic.base import TemplateResponseMixin
from django.views.generic import View
from courses.models import Course
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden


class ChatRoomView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = "chat/chat_room.html"

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        if course not in request.user.courses_joined.all():
            return HttpResponseForbidden()
        return self.render_to_response({"course": course})
