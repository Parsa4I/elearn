from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import InstructingRequest
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class InstructingRequestView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        if not (user.username and user.first_name and user.last_name):
            messages.info(
                request,
                "Please complete your profile before proceeding with your instructing request.",
            )
            return redirect("accounts:profile_complete")
        if not InstructingRequest.objects.filter(user=user).exists():
            InstructingRequest.objects.create(user=user)
            messages.success(
                request,
                "Your instrcuting request was sent successfully and will be reviewed soon.",
            )
        else:
            if InstructingRequest.objects.get(user=user).approved:
                messages.success(
                    request,
                    "Congratulations! You're now an instructor!",
                )
            else:
                messages.warning(
                    request,
                    "You have already sent a request.",
                )
        return redirect(reverse("accounts:profile", args=[request.user.pk]))
