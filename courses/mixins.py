from django.http import HttpResponseNotFound


class IsTeacherMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_teacher:
            return HttpResponseNotFound()
        return super().dispatch(request, *args, **kwargs)
