# configuracion/models.py
from django.db import models

class Aula(models.Model):
    nombre_aula = models.CharField(max_length=100)
    capacidad_aula = models.IntegerField()

    def __str__(self):
        return self.nombre_aula