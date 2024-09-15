from django.http.response import HttpResponse as HttpResponse
from django.views.generic import FormView, DetailView
from .forms import CourseCreateForm, ModuleCreateForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .mixins import IsTeacherMixin, IsCourseOwnerMixin
from .models import Course
from django.urls import reverse


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


class ModuleCreateView(IsCourseOwnerMixin, FormView):
    form_class = ModuleCreateForm
    template_name = "courses/module_create.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        slug = self.kwargs.get("slug")
        context["course"] = get_object_or_404(Course, slug=slug)
        return context

    def form_valid(self, form):
        module = form.save(commit=False)
        slug = self.kwargs.get("slug")
        course = get_object_or_404(Course, slug=slug)
        module.course = course
        module.save()
        return redirect(reverse("courses:detail", args=[slug]))
