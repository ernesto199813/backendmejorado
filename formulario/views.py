from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import RegistrationForm
from .serializers import RegistrationFormSerializer


class RegistrationFormListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
       
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
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# Asumo que tienes estos modelos y serializadores
# from .models import RegistrationForm
# from .serializers import RegistrationFormSerializer

# --- INICIO DE LA VISTA MODIFICADA ---

class RegistrationFormDetailView(APIView):
    """
    Gestiona la obtención, actualización y eliminación de un formulario de registro.
    Envía una notificación por correo electrónico cuando el email del formulario es modificado.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        """
        Obtiene el objeto RegistrationForm, asegurándose de que pertenece
        al usuario autenticado para mayor seguridad.
        """
        # CORRECCIÓN DE SEGURIDAD:
        # Filtramos por clave primaria (pk) Y por el usuario (user).
        # Esto previene que un usuario pueda acceder o modificar los datos de otro.
        return get_object_or_404(RegistrationForm, pk=pk, user=user)

    def get(self, request, pk, format=None):
        """ Maneja solicitudes GET para obtener un formulario específico. """
        registration_form = self.get_object(pk, request.user)
        serializer = RegistrationFormSerializer(registration_form)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        """
        Maneja actualizaciones parciales (PATCH).
        Si el campo 'email' se modifica, envía un correo de notificación.
        """
        registration_form = self.get_object(pk, request.user)
        
        # Guardamos el email original antes de cualquier modificación.
        # Asumimos que el campo en tu modelo se llama 'email'.
        original_email = registration_form.email
        
        serializer = RegistrationFormSerializer(
            instance=registration_form,
            data=request.data,
            partial=True, # Permite actualización parcial
            context={'request': request}
        )
        
        if serializer.is_valid():
            updated_form = serializer.save()
            
            # --- LÓGICA DE ENVÍO DE CORREO ---
            # Comprobamos si el email fue parte de los datos enviados Y si es diferente al original.
            if 'email' in request.data and updated_form.email != original_email:
                asunto = 'Actualización de datos de registro'
                mensaje = (
                    'Hola,\n\n'
                    'Te informamos que la dirección de correo electrónico asociada a tu registro ha sido actualizada.\n'
                    f'La nueva dirección es: {updated_form.email}\n\n'
                    'Si no reconoces esta actividad, por favor, ponte en contacto con nosotros inmediatamente.\n\n'
                    'Saludos.'
                )
                remitente = settings.EMAIL_HOST_USER
                
                try:
                    # Enviamos el correo a la NUEVA dirección.
                    send_mail(asunto, mensaje, remitente, [updated_form.email])
                    print(f"Correo de notificación enviado a {updated_form.email}") # Log para depuración
                except Exception as e:
                    # En un entorno real, deberías registrar este error.
                    print(f"ERROR: No se pudo enviar el correo de notificación. Error: {e}")
            
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # ... (tus métodos put y delete pueden permanecer igual) ...

    def put(self, request, pk, format=None):
        """
        Maneja solicitudes PUT para actualizar completamente un formulario.
        """
        # Nota: La lógica de email no se añade aquí, pero podría hacerse
        # siguiendo el mismo patrón que en el método PATCH si lo necesitas.
        registration_form = self.get_object(pk, request.user)
        serializer = RegistrationFormSerializer(
            instance=registration_form,
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """ Maneja solicitudes DELETE para eliminar un formulario específico. """
        registration_form = self.get_object(pk, request.user)
        registration_form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    
    

###########################################################################################

from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def enviar_correo_prueba(request):
    asunto = "Prueba de correo Django"
    mensaje = "¡Funciona correctamente! Este es un correo de prueba."
    remitente = settings.EMAIL_HOST_USER
    destinatario = [remitente]  # Enviar a ti mismo para probar

    try:
        send_mail(
            asunto,
            mensaje,
            remitente,
            destinatario,
            fail_silently=False,
        )
        return HttpResponse("¡Correo enviado correctamente!")
    except Exception as e:
        return HttpResponse(f"Error al enviar: {str(e)}")
