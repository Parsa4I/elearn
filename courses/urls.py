from django.urls import path
from . import views


app_name = "courses"

urlpatterns = [
    path("create/", views.CourseCreateView.as_view(), name="create"),
    path("<slug:slug>/", views.CourseDetailView.as_view(), name="detail"),
    path(
        "<slug:slug>/module/create/",
        views.ModuleCreateView.as_view(),
        name="module_create",
    ),
]
