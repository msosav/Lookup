from email.policy import default
from django.db import models

# Create your models here.


class Producto (models.Model):
    nombre = models.CharField(max_length=50)
    price = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    recomendado = models.BooleanField(default=True)
    categoria = models.CharField(max_length=50, default="N/A")
