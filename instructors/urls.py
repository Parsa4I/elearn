from django.urls import path
from . import views

app_name = "instructors"

urlpatterns = [
    path("request/", views.InstructingRequestView.as_view(), name="request"),
]
