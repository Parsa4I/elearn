from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("instructors/", include("instructors.urls")),
    path("stars/", include("stars.urls")),
    path("comments/", include("comments.urls")),
    path("chat/", include("chat.urls")),
    path("", TemplateView.as_view(template_name="base.html"), name="home"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
