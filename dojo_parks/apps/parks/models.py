from django.db import models
from apps.login.models import *

class Park(models.Model):
    title = models.CharField(max_length=90)
    address = models.CharField(max_length=180)
    review = models.TextField()
    rating = models.IntegerField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    added_by = models.ForeignKey(User, related_name="parks_added")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)