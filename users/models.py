from django.contrib.auth.models import AbstractUser
from django.db import models


USER_TYPE_CHOICES = (
    ('user', 'User'),
    ('clinic', 'Clinic'),
    ('seller', 'Seller'),
    ('admin', 'Admin'),
)
class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    is_seller = models.BooleanField(default=False)
    is_clinic = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.user_type = 'admin'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
