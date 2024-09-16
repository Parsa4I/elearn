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
    path(
        "module/<int:pk>/item/<str:item_type>/create/",
        views.ContentCreateUpdateView.as_view(),
        name="content_create",
    ),
    path(
        "module/<int:pk>/item/<str:item_type>/update/<int:item_id>",
        views.ContentCreateUpdateView.as_view(),
        name="content_update",
    ),
]
