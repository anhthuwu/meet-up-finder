import datetime
from django.db import models
from django.db.models import IntegerField, Model

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    date = models.DateField('date')
    time = models.TimeField('time')
    host = models.CharField(max_length=50)
    rating = models.IntegerField()
    description = models.CharField(default = 'none',max_length=500)
    addedTOMyEvent = models.BooleanField(default=False)
    lng = models.FloatField(default=-78.5080)
    lat = models.FloatField(default=38.0336)

    def __str__(self):
        return self.name

from django.contrib.auth.models import User

class Location(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(default='University of Virginia', max_length=100)
    lat = models.FloatField(default=38.0336, max_length=100)
    lng = models.FloatField(default=-78.5080, max_length=100)
    distance = models.IntegerField(default = 1000)