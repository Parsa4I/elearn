from django.views.generic import FormView
from .forms import CourseCreateForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .mixins import IsTeacherMixin


class CourseCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = CourseCreateForm
    template_name = "courses/create_course.html"

    def form_valid(self, form):
        course = form.save(commit=False)
        course.slug = slugify(course.title)
        course.teacher = self.request.user
        course.save()
        messages.success(self.request, f"Course {course.title} created successfully.")
        return redirect("home")
