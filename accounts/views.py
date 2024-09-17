from django.views.generic import FormView, View, DetailView
from .forms import LoginForm, SignupForm, ProfileCompleteForm
from django.views.generic.base import TemplateResponseMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.urls import reverse


class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        user = authenticate(
            self.request,
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )
        login(self.request, user)
        return redirect("home")


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("home")


class SignupView(FormView):
    form_class = SignupForm
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        cd = form.cleaned_data
        user = User.objects.create_user(email=cd["email"], password=cd["password1"])
        login(self.request, user)
        return redirect("home")


class ProfileCompleteView(TemplateResponseMixin, LoginRequiredMixin, View):
    template_name = "accounts/profile_complete.html"
    form_class = ProfileCompleteForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return self.render_to_response({"form": form})

    def post(self, request):
        form = self.form_class(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("accounts:profile", args=[self.request.user.pk]))
        return self.render_to_response({"form": form})


class ProfileView(DetailView):
    template_name = "accounts/profile.html"
    queryset = User.objects.all()
    context_object_name = "user"
