from django.db import models
from django.utils import timezone  
import datetime

# Create your models here.
class EventoCalendario(models.Model):
    titulo = models.CharField(max_length=200)
    fecha = models.DateField(default=timezone.now)  # Añade default=timezone.now
    hora_inicio = models.TimeField(default=datetime.time(0, 0, 0))
    hora_fin = models.TimeField(default=datetime.time(12, 0, 0))
    salon = models.CharField(max_length=100, default='Sin salón asignado')
    def __str__(self):
        return self.titulo