from django.db import models
from users.models import CustomUser  # Correct import

class VetClinic(models.Model):
    owner   = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'clinic'})
    name    = models.CharField(max_length=200)
    address = models.TextField()
    map_link= models.URLField(blank=True)
    phone   = models.CharField(max_length=20, blank=True)
    def __str__(self): return self.name

class Doctor(models.Model):
    clinic = models.ForeignKey(VetClinic, on_delete=models.CASCADE)
    name   = models.CharField(max_length=120)
    specialization = models.CharField(max_length=120, blank=True)
    fee    = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    def __str__(self): return f"{self.name} @ {self.clinic.name}"

class TimeSlot(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start  = models.DateTimeField()
    end    = models.DateTimeField()
    is_available = models.BooleanField(default=True)
    def __str__(self): return f"{self.doctor.name} {self.start:%Y-%m-%d %H:%M}"
