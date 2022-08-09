from django.db import models

# Create your models here.

class Producto (models.Model):
    nombre = models.TextField(max_length=50)
    price = models.FloatField()
    rating = models.FloatField()