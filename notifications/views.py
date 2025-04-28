from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification  # Changed from Notificacion
from .serializers import NotificationSerializer, MarkAsReadSerializer  # Changed from NotificacionSerializer, MarcarComoLeidaSerializer


class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).select_related('form')
        # Changed usuario→user, formulario→form

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Changed usuario→user


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).select_related('form')
        # Changed usuario→user, formulario→form


class MarkAsReadView(generics.UpdateAPIView):
    serializer_class = MarkAsReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)  # Changed usuario→user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data['read']:  # Changed leida→read
            instance.mark_as_read()  # Changed marcar_como_leida→mark_as_read
        else:
            instance.read = False  # Changed leida→read
            instance.read_date = None  # Changed fecha_lectura→read_date
            instance.save()

        return Response(NotificationSerializer(instance).data)