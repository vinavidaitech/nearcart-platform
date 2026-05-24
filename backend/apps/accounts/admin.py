from django.contrib import admin
from .models import CustomUser, StaffMembership
from unfold.admin import ModelAdmin, StackedInline, TabularInline


# Register your models here
# admin.site.register(CustomUser)
# admin.site.register(StaffMembership)

# -- IMPORTANT: registered in inventory admin.py file

from django.contrib.auth.admin import UserAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from apps.accounts.models import CustomUser, StaffMembership


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = [
        "email",
        "full_name",
        "role",
        "is_active",
        "is_verified",
        "is_staff",
        "created_at",
    ]
    list_filter = ["role", "is_active", "is_verified", "is_staff"]
    search_fields = ["email", "full_name", "phone"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("full_name", "phone", "avatar_url")}),
        (
            "Role & access",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Preferences", {"fields": ("preferred_radius_km",)}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "role", "password1", "password2"),
            },
        ),
    )


@admin.register(StaffMembership)
class StaffMembershipAdmin(ModelAdmin):
    list_display = [
        "user",
        "shop",
        "permission_level",
        "invited_by",
        "joined_at",
        "is_active",
    ]
    list_filter = ["permission_level", "is_active", "shop"]
    search_fields = ["user__email", "user__full_name", "shop__name"]
    readonly_fields = ["joined_at"]
