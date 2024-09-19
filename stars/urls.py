from django.urls import path
from . import views


app_name = "stars"

urlpatterns = [
    path("rate/<slug:slug>/", views.RateCourseView.as_view(), name="rate"),
]
