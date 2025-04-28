from rest_framework import serializers
from .models import EventoCalendario
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EventoCalendarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventoCalendario
        fields = ['id', 'titulo', 'fecha', 'hora_inicio', 'hora_fin', 'salon']


