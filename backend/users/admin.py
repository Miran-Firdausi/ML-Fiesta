# admin.py
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    # List the fields to be displayed in the user list page in admin
    list_display = ("email", "full_name", "is_active", "is_staff", "is_superuser")

    # Allow filtering by certain fields
    list_filter = ("is_active", "is_staff", "is_superuser")

    # Add search functionality based on email
    search_fields = ("email", "full_name")

    # Allow adding and editing the `full_name` and `email` fields in the admin
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
