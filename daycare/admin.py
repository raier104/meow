# from django.contrib import admin
# from .models import Daycare

from django.contrib import admin
from .models import Daycare

@admin.register(Daycare)
class DaycareAdmin(admin.ModelAdmin):
	list_display = ("name", "address", "phone")
