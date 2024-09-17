from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email", "username", "is_admin", "is_instructor")
    list_filter = ("is_admin", "is_active", "is_instructor")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "is_instructor",
                    "username",
                    "first_name",
                    "last_name",
                )
            },
        ),
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
                "fields": ("email", "password1", "password2", "is_instructor"),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("-last_login", "email")
