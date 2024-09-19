from django.views.generic import View
from courses.models import Course
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Star
from django.db.utils import IntegrityError
from .forms import StarsForm
from django.urls import reverse
from django.contrib import messages


class RateCourseView(LoginRequiredMixin, View):
    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        form = StarsForm(request.POST)
        if form.is_valid():
            try:
                Star.objects.create(
                    user=request.user,
                    content_object=course,
                    points=form.cleaned_data["rating"],
                )
                messages.success(request, "Rating received. Thank you.")
            except IntegrityError:
                messages.error(request, "You've already rated this course.")
        return redirect(reverse("courses:detail", args=[course.slug]))
