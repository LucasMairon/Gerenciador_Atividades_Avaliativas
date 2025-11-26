from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User
from .forms import CustomUserCreationAdminForm, CustomUserChangeAdminForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    ordering = ['name']
    add_form = CustomUserCreationAdminForm
    form = CustomUserChangeAdminForm

    list_display = ('institutional_email', 'name')

    fieldsets = (
        (None, {'fields': ('name', 'institutional_email',
         'personal_email', 'campus', 'department', 'password')}),
        ('Permissões', {'fields': ('is_active',
         'is_staff', 'is_superuser', 'groups')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('name', 'institutional_email', 'campus', 'department', 'password1', 'password2')
        }),
    )

    list_filter = ['is_superuser']
    search_fields = ('institutional_email', 'name')
