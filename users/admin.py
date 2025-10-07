from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'user_type', 'is_seller', 'is_clinic', 'is_approved', 'is_staff')
    list_filter = ('user_type', 'is_seller', 'is_clinic', 'is_approved', 'is_staff')
    actions = ['approve_seller_users', 'approve_clinic_users']

    def approve_seller_users(self, request, queryset):
        updated = queryset.filter(is_seller=True).update(is_approved=True)
        self.message_user(request, f'{updated} seller user(s) approved successfully.')

    def approve_clinic_users(self, request, queryset):
        updated = queryset.filter(is_clinic=True).update(is_approved=True)
        self.message_user(request, f'{updated} clinic user(s) approved successfully.')
