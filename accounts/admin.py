from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()

admin.site.unregister(Group)


class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ['email', 'admin']
    list_filter = ['admin']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password', 'password_2')}
         ),
    )

    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
