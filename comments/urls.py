from django.urls import path
from . import views


app_name = "comments"

urlpatterns = [
    path(
        "comment-course/<slug:slug>/",
        views.CommentCourseView.as_view(),
        name="comment_course",
    ),
]
