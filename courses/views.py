from typing import Any
from django.db.models.base import Model as Model
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import FormView, DetailView, View, ListView
from django.views.generic.base import TemplateResponseMixin
from .forms import CourseCreateForm, ModuleCreateForm
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .mixins import IsTeacherMixin, IsCourseOwnerMixin
from .models import Course, Module, Text, Image, Video, File
from django.urls import reverse
from django.forms import modelform_factory
from django.apps import apps
from django.http import HttpResponseNotFound, HttpResponseForbidden
from itertools import chain
from stars.forms import StarsForm
from stars.models import Star
from django.db.models.aggregates import Avg
from comments.forms import CommentForm
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery


class CourseCreateView(LoginRequiredMixin, IsTeacherMixin, FormView):
    form_class = CourseCreateForm
    template_name = "courses/course_create.html"

    def form_valid(self, form):
        course = form.save(commit=False)
        course.slug = slugify(course.title)
        course.teacher = self.request.user
        course.save()
        course.students.add(self.request.user)
        messages.success(self.request, f"Course {course.title} created successfully.")
        return redirect(course.get_absolute_url())


class CourseDetailView(DetailView):
    queryset = Course.objects.prefetch_related("modules").prefetch_related("comments")
    template_name = "courses/course_detail.html"
    context_object_name = "course"
    lookup_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StarsForm()

        rated = False
        if self.request.user.is_authenticated:
            rated = Star.objects.filter(
                content_type__model="course",
                user=self.request.user,
                object_id=context["course"].pk,
            ).exists()
        context["rated"] = rated
        
        avg_rate = cache.get(f"course_{context["course"].pk}_avg_rate")
        if not avg_rate:
            avg_rate = Star.objects.filter(
                content_type__model="course", object_id=context["course"].pk
            ).aggregate(points=Avg("points"))["points"]
            cache.set(f"course_{context["course"].pk}_avg_rate", avg_rate, timeout=60 * 60)

        context["avg_rate"] = avg_rate
        context["comment_form"] = CommentForm()

        return context


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
        
        key = make_template_fragment_key("modules", [course.pk])
        cache.delete(key)

        return redirect(reverse("courses:module_detail", args=[module.pk]))


class ModuleDetailView(DetailView):
    queryset = (
        Module.objects.prefetch_related("text_items")
        .prefetch_related("image_items")
        .prefetch_related("video_items")
        .prefetch_related("file_items")
    )
    template_name = "courses/module_detail.html"
    context_object_name = "module"

    def get_sorted_items(self, module):
        sorted_items = cache.get(f"module_{module.pk}_items")
        if not sorted_items:
            module = self.get_object()
            text_items = module.text_items.all()
            image_items = module.image_items.all()
            video_items = module.video_items.all()
            file_items = module.file_items.all()

            items = list(chain(text_items, image_items, video_items, file_items))
            items = sorted(items, key=lambda item: item.order)

            cache.set(f"module_{module.pk}_items", items, timeout=60 * 5)

            return items
        return sorted_items


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = self.get_sorted_items(context["module"])
        return context


class ItemCreateUpdateView(TemplateResponseMixin, View):
    template_name = "courses/item_create_update.html"

    def dispatch(self, request, *args, **kwargs):
        module = get_object_or_404(Module, pk=kwargs["pk"])
        if module.course.teacher != request.user:
            return HttpResponseForbidden()
        return super().dispatch(request, *args, **kwargs)

    def get_model(self, model_name):
        if model_name.lower() in ["text", "image", "video", "file"]:
            return apps.get_model("courses", model_name.lower())
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


class ItemDetailView(DetailView):
    template_name = "courses/item_detail.html"
    context_object_name = "item"

    def dispatch(self, request, *args, **kwargs):
        item = get_object_or_404(
            apps.get_model("courses", kwargs["item_type"].lower()), pk=kwargs["pk"]
        )
        if (
            request.user not in item.module.course.students.all()
            and request.user != item.module.course.teacher
        ):
            return HttpResponseForbidden(
                f"You do not have access to contents of this course. <a href='{reverse('courses:detail', args=[item.module.course.slug])}'>Enroll</a>"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        item_type = self.kwargs["item_type"]
        if item_type == "text":
            return Text.objects.all()
        elif item_type == "image":
            return Image.objects.all()
        elif item_type == "video":
            return Video.objects.all()
        elif item_type == "file":
            return File.objects.all()
        return None


def download_file(request, file_pk):
    file_obj = get_object_or_404(File, pk=file_pk)

    filename = file_obj.file.name.split("/")[-1]
    response = HttpResponse(file_obj.file, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


class CourseEnroll(LoginRequiredMixin, View):
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        if request.user not in course.students.all():
            course.students.add(request.user)
            messages.success(request, f"You have been enrolled in {course}.")
            return redirect(reverse("courses:detail", args=[course.slug]))
        messages.error(request, f"You have already been enrolled in {course}.")
        return redirect(reverse("courses:detail", args=[course.slug]))


class CourseListView(ListView):
    queryset = Course.objects.all()
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 4

    def get_queryset(self):
        q = self.request.GET.get("q")
        queryset = super().get_queryset()
        if q:
            vector = (
                SearchVector("title", weight="A") +
                SearchVector("overview", weight="A") +
                SearchVector("teacher__username", weight="B") +
                SearchVector("teacher__email", weight="C") +
                SearchVector("subject__title", weight="B") +
                SearchVector("teacher__first_name", weight="D") +
                SearchVector("teacher__last_name", weight="D")
            )
            query = SearchQuery(q)

            queryset = queryset.annotate(
                search=vector,
                rank=SearchRank(vector, query)
            ).filter(
                search=query
            ).order_by(
                "-rank"
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context
