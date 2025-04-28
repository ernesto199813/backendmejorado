from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

User = get_user_model()

def validate_id_number(value):
    """
    Valida que el número de cédula tenga el formato: V/E seguido de 6 a 8 dígitos
    Ejemplos válidos: V123456, E1234567, V12345678
    """
    pattern = r'^[VEve]\d{6,8}$'
    if not re.match(pattern, value):
        raise ValidationError(
            'La cédula debe comenzar con V o E seguido de 6 a 8 dígitos (ej: V123456, E12345678)'
        )

class RegistrationForm(models.Model):
    # Personal Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forms')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_number = models.CharField(
        max_length=9,  # V/E (1) + máximo 8 dígitos
        unique=True,
        validators=[validate_id_number],
        verbose_name="Cédula",
        help_text="Formato: V o E seguido de 6 a 8 dígitos (ej: V123456, E12345678)"
    )
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    academic_degree = models.CharField(max_length=50)
    state_of_residence = models.CharField(max_length=50)
    
    # State field
    STATE_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]
    state = models.CharField(
        max_length=10,
        choices=STATE_CHOICES,
        default='pendiente',
        verbose_name="Form State"
    )
    
    # Regulated Subject Information
    REGULATED_CHOICES = [
        ('si', 'Si'),
        ('no', 'No'),
    ]
    is_regulated_subject = models.CharField(
        max_length=3,
        choices=REGULATED_CHOICES,
        verbose_name="Is regulated subject?",
        help_text="Select if you are a regulated subject or not"
    )
    
    regulated_subject_type = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="Regulated subject type",
        help_text="Required if regulated subject"
    )
    intermediary_type = models.CharField(max_length=50, blank=True, null=True)
    auxiliary_type = models.CharField(max_length=50, blank=True, null=True)
    auditor_type = models.CharField(max_length=50, blank=True, null=True)
    registration_code = models.CharField(max_length=50, blank=True, null=True)
    
    # Information for non-regulated subjects
    employment_condition = models.CharField(
        max_length=50, 
        blank=True, 
        null=True,
        verbose_name="Employment condition",
        help_text="Required if not a regulated subject"
    )
    
    # Additional information
    company_type = models.CharField(max_length=50)
    years_of_experience = models.CharField(max_length=20)
    desired_diploma = models.CharField(max_length=50)
    employment_status = models.CharField(max_length=50)
    comments = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registration Form"
        verbose_name_plural = "Registration Forms"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.id_number}"

    def clean(self):
        """Normaliza la cédula a mayúsculas"""
        if self.id_number:
            self.id_number = self.id_number.upper()
        super().clean()




  
   
  