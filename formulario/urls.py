from django.urls import path
from .views import RegistrationFormListCreateView, RegistrationFormDetailView,enviar_correo_prueba   # Corrected imports

urlpatterns = [
    path('formularios/', RegistrationFormListCreateView.as_view(), name='formulario-list'),  # Corrected class name
    path('formularios/<int:pk>/', RegistrationFormDetailView.as_view(), name='formulario-detail'),  # Corrected class name
    path('probar-correo/', enviar_correo_prueba, name='probar_correo'),
]


