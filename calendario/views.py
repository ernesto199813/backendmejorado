from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import EventoCalendario
from .serializers import EventoCalendarioSerializer
from django.shortcuts import get_object_or_404
from datetime import datetime

class EventoCalendarioView(APIView):
    def get(self, request):
        eventos = EventoCalendario.objects.all()
        serializer = EventoCalendarioSerializer(eventos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventoCalendarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        evento = get_object_or_404(EventoCalendario, pk=pk)
        serializer = EventoCalendarioSerializer(evento, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        evento = get_object_or_404(EventoCalendario, pk=pk)
        evento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)