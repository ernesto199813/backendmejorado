# configuracion/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Aula
from .serializers import AulaSerializer
from django.shortcuts import get_object_or_404

class AulaView(APIView):  # Renamed to AulaView
    def get(self, request):
        aulas = Aula.objects.all()
        serializer = AulaSerializer(aulas, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AulaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        aula = get_object_or_404(Aula, pk=pk)
        serializer = AulaSerializer(aula, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        aula = get_object_or_404(Aula, pk=pk)
        aula.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)