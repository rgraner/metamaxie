import django
from django.contrib import admin
from .models import User, Manager, Scholar, ManagerTeam, ScholarTeam
from .forms import RegistrationForm
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = User
    add_form = RegistrationForm
    list_display = ('username', 'type')

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'use role',
            {
                'fields': (
                    'type',
                    'avatar',
                )
            
            }
        )

    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Manager)
admin.site.register(ManagerTeam)
admin.site.register(Scholar)
admin.site.register(ScholarTeam)
