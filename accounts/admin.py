from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode


# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin', )

    fieldsets = (
        (None, {'fields' : ('email', 'phone_number', 'full_name', 'password')}),
        ('Permission', {'fields': ('is_active', 'is_admin', 'last_login')})
    )

    add_fieldsets = (
        (None, {'fields' : ('phone_number', 'email', 'full_name', 'password1', 'password2')}),
    )

    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(OtpCode)