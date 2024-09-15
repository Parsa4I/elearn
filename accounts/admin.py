from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email", "username", "is_admin", "is_teacher")
    list_filter = ("is_admin", "is_active", "is_teacher")
    fieldsets = (
        (None, {"fields": ("email", "password", "is_teacher")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_teacher"),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("-last_login", "email")
