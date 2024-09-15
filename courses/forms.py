from django import forms
from .models import Course, Module


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "overview", "subject"]


class ModuleCreateForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["title", "description"]
