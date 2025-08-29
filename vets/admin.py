from django.contrib import admin
from .models import VetClinic, Doctor, TimeSlot
admin.site.register([VetClinic, Doctor, TimeSlot])