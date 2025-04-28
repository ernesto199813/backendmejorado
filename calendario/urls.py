from django.urls import path
from .views import EventoCalendarioView  # Importa solo FormularioView

urlpatterns = [
    path('calendario/', EventoCalendarioView.as_view(), name='calendario'),
    path('calendario/<int:pk>/', EventoCalendarioView.as_view(), name='calendario-detail'), # URL para actualizar y eliminar


]