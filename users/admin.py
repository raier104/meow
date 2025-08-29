from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'is_seller', 'is_approved', 'is_staff')
    list_filter = ('is_seller', 'is_approved', 'is_staff')
    actions = ['approve_seller_users']  # Use a list, not a tuple

    def approve_seller_users(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} seller user(s) approved successfully.')
