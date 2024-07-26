from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=13)
    birth_date = models.DateField(null=True, blank=True)
    sites = models.JSONField(default=dict, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    profile_image = models.ImageField(upload_to='images/profile_image/', blank=True)


    def __str__(self):
        return self.username


