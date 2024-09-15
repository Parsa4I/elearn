from django.views.generic import FormView, DetailView
from .forms import CourseCreateForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .mixins import IsTeacherMixin
from .models import Course


class CourseCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = CourseCreateForm
    template_name = "courses/course_create.html"

    def form_valid(self, form):
        course = form.save(commit=False)
        course.slug = slugify(course.title)
        course.teacher = self.request.user
        course.save()
        messages.success(self.request, f"Course {course.title} created successfully.")
        return redirect("courses:detail")


class CourseDetailView(DetailView):
    queryset = Course.objects.all()
    template_name = "courses/course_detail.html"
    context_object_name = "course"
    lookup_field = "slug"
