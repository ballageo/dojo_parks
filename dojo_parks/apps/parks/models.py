from django.db import models
from apps.login.models import *

# Create your models here


class Park (models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    review = models.TextField
    rating = models.IntegerField()
    longitude = models.IntegerField()
    latitude = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    created_by = models.ForeignKey(User, related_name="parks_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)