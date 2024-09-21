from django.views.generic import View
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from courses.models import Course
from django.views.generic.base import TemplateResponseMixin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key


class CommentCourseView(TemplateResponseMixin, LoginRequiredMixin, View):
    template_name = "courses/course_detail.html"

    def post(self, request, slug):
        form = CommentForm(request.POST)
        if form.is_valid():
            course = get_object_or_404(Course, slug=slug)
            comment = form.save(commit=False)
            comment.content_object = course
            comment.user = request.user
            comment.save()

            key = make_template_fragment_key("comments", [course.pk])
            cache.delete(key)

            return redirect(course.get_absolute_url())
        return self.render_to_response({"comment_form": form})
