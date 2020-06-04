from django.db import models

# Create your models here.

class Image(models.Model):
    image = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    probability = models.FloatField()