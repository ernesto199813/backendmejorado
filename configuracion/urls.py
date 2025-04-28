# configuracion/urls.py
from django.urls import path
from .views import AulaView  # Import the correct view

urlpatterns = [
    path('aulas/', AulaView.as_view(), name='aulas'),  # POST and GET
    path('aulas/<int:pk>/', AulaView.as_view(), name='aulas-detail'), # PUT and DELETE
]