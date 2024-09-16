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
        views.ItemCreateUpdateView.as_view(),
        name="item_create",
    ),
    path(
        "module/<int:pk>/item/<str:item_type>/update/<int:item_id>",
        views.ItemCreateUpdateView.as_view(),
        name="item_update",
    ),
    path("module/<int:pk>/", views.ModuleDetailView.as_view(), name="module_detail"),
    path(
        "item/<str:item_type>/<int:pk>/",
        views.ItemDetailView.as_view(),
        name="item_detail",
    ),
    path(
        "download/<int:file_pk>/",
        views.download_file,
        name="download_file",
    ),
]
