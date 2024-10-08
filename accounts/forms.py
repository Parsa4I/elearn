from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ValidationError


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "email",
        ]

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords must match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "username", "is_active", "is_admin"]


class LoginForm(forms.Form):
    email = forms.CharField(label="Email/Username")
    password = forms.CharField(widget=forms.PasswordInput)


class SignupForm(forms.Form):
    email = forms.CharField()
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    def clean_password2(self):
        pw1 = self.cleaned_data["password1"]
        pw2 = self.cleaned_data["password2"]
        if pw1 and pw2 and pw1 != pw2:
            raise ValidationError("Passwords must match.")
        return pw2


class ProfileCompleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name"]
