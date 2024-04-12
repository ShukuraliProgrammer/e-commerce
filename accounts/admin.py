from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from accounts.models import *

admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display =  ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "address", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

@admin.register(VerifictionOtp)
class VerificationOtp(admin.ModelAdmin):
    list_display = ['id', 'user', 'code', 'expires_in']


@admin.register(UserAddress)
class UserAddress(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'street']
