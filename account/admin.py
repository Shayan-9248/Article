from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, Group
from .forms import *
from .models import *


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('email', 'username', 'is_active', 'is_admin', 'is_superuser', 'is_author', 'is_special_user')
    list_filter = ('is_active', 'is_author')
    fieldsets = (
        ('user', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('is_active',)}),
        ('Special Fields', {'fields': ('is_author', 'special_user',)}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Super User', {'fields': ('is_superuser',)})
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'username', 'password1', 'password2')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.unregister(Group)