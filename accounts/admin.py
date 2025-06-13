from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin', )

    fieldsets = (
        (None, {'fields' : ('email', 'phone_number', 'full_name', 'password')}),
        ('Permission', {'fields': ('is_active', 'is_admin', 'last_login', 'groups', 'user_permissions')})
    )

    add_fieldsets = (
        (None, {'fields' : ('phone_number', 'email', 'full_name', 'password1', 'password2')}),
    )

    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)