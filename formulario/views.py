from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import RegistrationForm
from .serializers import RegistrationFormSerializer

# Asumiendo que tienes un modelo RegistrationForm y un serializer RegistrationFormSerializer
# definidos en alguna parte de tu app.

# Vista para listar y crear formularios
class RegistrationFormListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Asumiendo que 'forms' es el related_name en el modelo User para RegistrationForm
        # o que tienes una lógica similar para obtener los forms del usuario.
        # Si no tienes related_name, podrías hacer:
        # forms = RegistrationForm.objects.filter(user=request.user) este es para usuarios que haya registrado y solo puedan visualizar los registros que ellos hicieron
        forms =  RegistrationForm.objects.all()
        #forms = request.user.forms.all() # 
        serializer = RegistrationFormSerializer(forms, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RegistrationFormSerializer(
            data=request.data,
            context={'request': request} # Pasar request al contexto si es necesario en el serializer
        )

        if serializer.is_valid():
            # Asigna el usuario autenticado automáticamente al guardar
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vista para ver, actualizar (completo y parcial) y eliminar un formulario específico
class RegistrationFormDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        """
        Obtiene el objeto RegistrationForm asegurándose de que pertenece
        al usuario autenticado.
        """
        # Usamos get_object_or_404 para manejar el caso de que no exista el pk
        # y filtramos por el usuario para seguridad.
        return get_object_or_404(RegistrationForm, pk=pk)

    def get(self, request, pk, format=None):
        """ Maneja solicitudes GET para obtener un formulario específico. """
        registration_form = self.get_object(pk, request.user)
        serializer = RegistrationFormSerializer(registration_form)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        Maneja solicitudes PUT para actualizar completamente un formulario.
        Requiere que se envíen TODOS los campos requeridos.
        """
        registration_form = self.get_object(pk, request.user)
        serializer = RegistrationFormSerializer(
            instance=registration_form, # Importante pasar la instancia a actualizar
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            # No necesitas pasar user=request.user aquí porque ya está en la instancia
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # --- MÉTODO PATCH AÑADIDO ---
    def patch(self, request, pk, format=None):
       
        registration_form = self.get_object(pk, request.user)
        
        serializer = RegistrationFormSerializer(
            instance=registration_form, # La instancia existente
            data=request.data,          # Los datos parciales a actualizar
            partial=True,               # ¡Importante! Permite actualización parcial
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # --- FIN MÉTODO PATCH ---

    def delete(self, request, pk, format=None):
        """ Maneja solicitudes DELETE para eliminar un formulario específico. """
        registration_form = self.get_object(pk, request.user)
        registration_form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)