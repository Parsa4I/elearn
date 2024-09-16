from django.http.response import HttpResponse as HttpResponse
from django.views.generic import FormView, DetailView, View
from django.views.generic.base import TemplateResponseMixin
from .forms import CourseCreateForm, ModuleCreateForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .mixins import IsTeacherMixin, IsCourseOwnerMixin
from .models import Course, Module
from django.urls import reverse
from django.forms import modelform_factory
from django.apps import apps
from django.http import HttpResponseNotFound


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


class ContentCreateUpdateView(TemplateResponseMixin, View):
    template_name = "courses/content_create_update.html"

    def get_model(self, model_name):
        if model_name in ["text", "image", "video", "file"]:
            return apps.get_model("courses", model_name)
        return None

    def get(self, request, pk, item_type, item_id=None):
        get_object_or_404(Module, pk=pk)
        model = self.get_model(item_type)
        if not model:
            return HttpResponseNotFound()
        item = None
        if item_id:
            item = get_object_or_404(model, pk=item_id)
        form = modelform_factory(
            model, exclude=["created", "updated", "order", "module"]
        )(instance=item)
        return self.render_to_response({"form": form, "item": item})

    def post(self, request, pk, item_type, item_id=None):
        model = self.get_model(item_type)
        if not model:
            return HttpResponseNotFound()
        item = None
        if item_id:
            item = get_object_or_404(model, pk=item_id)
        form = modelform_factory(
            model, exclude=["created", "updated", "order", "module"]
        )(instance=item, data=request.POST, files=request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.module = get_object_or_404(Module, pk=pk)
            item.save()
            return redirect(reverse("courses:detail", args=[item.module.course.slug]))
        return self.render_to_response({"form": form, "item": item})
