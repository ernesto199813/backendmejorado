from django.db import models
from django.contrib.auth import get_user_model
from formulario.models import RegistrationForm 
from django.utils import timezone  

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('form', 'New Form'),
        ('approval', 'Approval'),
        ('rejection', 'Rejection'),
        ('general', 'General'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=100)
    message = models.TextField()
    read = models.BooleanField(default=False)
    form = models.OneToOneField(  # Cambiado de ForeignKey a OneToOneField
        RegistrationForm,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        unique=True,  # Esto garantiza una sola notificación por formulario
        related_name='notification'  # Cambiado a singular para reflejar relación 1-a-1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Notifications'
        constraints = [
            models.UniqueConstraint(
                fields=['form'],
                name='unique_notification_per_form'
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def mark_as_read(self):
        if not self.read:
            self.read = True
            self.read_at = timezone.now()
            self.save()