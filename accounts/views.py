from django.views.generic import FormView
from .forms import LoginForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login


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
        return render(self.request, "accounts/logged_in.html")
