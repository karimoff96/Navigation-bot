from django.db import models
from model_utils.models import TimeStampedModel


# Create your models here.
class User(TimeStampedModel, models.Model):
    user_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255, blank=True)
    step = models.IntegerField(default=0)
    choice = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    language = models.CharField(max_length=10, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class City(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Type(TimeStampedModel, models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Place(TimeStampedModel, models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    desc = models.TextField()
    
    def __str__(self) -> str:
        return self.name
