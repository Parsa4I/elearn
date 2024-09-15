from django.views.generic import FormView, View
from .forms import LoginForm, SignupForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model


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
        user = get_user_model().objects.create_user(
            email=cd["email"], password=cd["password1"]
        )
        login(self.request, user)
        return redirect("home")
