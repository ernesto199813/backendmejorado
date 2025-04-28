from django.db.models.signals import post_save
from django.dispatch import receiver
from formulario.models import RegistrationForm
from .models import Notification

@receiver(post_save, sender=RegistrationForm)
def create_notification_on_form_submission(sender, instance, created, **kwargs):
    if created:
        # Crea el mensaje de la notificación con los datos del formulario
        message = (
            f"Nueva postulacion {instance.first_name} {instance.last_name}\n"  # Changed nombre to first_name and apellido to last_name
            f"for the {instance.desired_diploma} diploma"  # changed diplomado_deseado to desired_diploma
        )

        Notification.objects.create(
            user=instance.user,  # Changed usuario to user
            type='form',
            title='Nueva Postulacion',
            message=message,
            form=instance
        )