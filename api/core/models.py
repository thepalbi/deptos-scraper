from django.db import models

# Create your models here.
class Property(models.Model):
    url = models.URLField()