from django.urls import path
from . import views


app_name = "courses"

urlpatterns = [
    path("create/", views.CourseCreateView.as_view(), name="create"),
]
