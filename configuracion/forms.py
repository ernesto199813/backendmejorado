# configuracion/forms.py
from django import forms
from .models import Aula

class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['nombre_aula', 'capacidad_aula']  # Exclude 'id' - it's auto-generated