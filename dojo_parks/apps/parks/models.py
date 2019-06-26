from django.db import models
from apps.login.models import *

# Create your models here


class Park (models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    review = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    longitude = models.DecimalField(max_digits=8, decimal_places=4)
    latitude = models.DecimalField(max_digits=8, decimal_places=4)
    operating_hours = models.TextField(blank=True)
    website = models.CharField(max_length=255, default="Sorry, no website found")
    phone_number = models.CharField(max_length=20, default="Sorry, no phone number found")
    created_by = models.ForeignKey(User, related_name="parks_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)