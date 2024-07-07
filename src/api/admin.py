from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import (
    Account,
    User,
    Mentor,
)


class UserModelAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",
                           "first_name", "last_name", "email",
                           "is_active", "is_staff", "is_superuser",
                           "groups", "user_permissions", "role",
                           "last_login", "date_joined", "phone"),
            },
        ),
    )


@admin.register(Account)
class UserAdmin(UserModelAdmin):
    show_on_dispaly = '__all__'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    show_on_dispaly = '__all__'


@admin.register(Mentor)
class MentorsAdmin(admin.ModelAdmin):
    show_on_dispaly = '__all__'
