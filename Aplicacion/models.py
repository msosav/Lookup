from email.policy import default
from django.db import models

# Create your models here.


class Producto (models.Model):
    nombre = models.CharField(max_length=50)
    price = models.IntegerField()
    rating = models.FloatField()
    recomendado = models.BooleanField(default=True)
    categoria = models.CharField(max_length=50, default="N/A")
    url = models.CharField(max_length=200, default="N/A")
    imagen = models.CharField(max_length=200, default="N/A")
