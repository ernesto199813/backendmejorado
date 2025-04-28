from rest_framework import serializers
from .models import Notification
from formulario.models import RegistrationForm  

class FormInfoSerializer(serializers.Serializer):
    """Serializador dedicado solo para la información del formulario"""
    first_name = serializers.CharField(source='form.first_name')
    last_name = serializers.CharField(source='form.last_name')
    desired_diploma = serializers.CharField(source='form.desired_diploma')
    created_at = serializers.DateTimeField(source='form.created_at')
    updated_at = serializers.DateTimeField(source='form.updated_at')

class NotificationSerializer(serializers.ModelSerializer):
    form_info = serializers.SerializerMethodField()
    form = serializers.PrimaryKeyRelatedField(
        queryset=RegistrationForm.objects.all(),
        required=False,
        allow_null=True
    )
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'type',
            'title',
            'message',
            'read',
            'created_at',
            'read_at',
            'form',
            'form_info',
            'user'
        ]
        read_only_fields = ['created_at', 'read_at', 'user', 'form_info']

    def get_form_info(self, obj):
        """Obtiene información detallada del formulario asociado"""
        if obj.form:
            return {
                'first_name': obj.form.first_name,
                'last_name': obj.form.last_name,
                'desired_diploma': obj.form.desired_diploma,
                'created_at': obj.form.created_at,
                'updated_at': obj.form.updated_at,
                'id_number': obj.form.id_number,  # Agregado para referencia
                'state': obj.form.state  # Agregado para estado del formulario
            }
        return None

    def validate(self, data):
        """Validaciones adicionales"""
        valid_types = ['form', 'approval', 'rejection', 'general']
        if data.get('type') not in valid_types:
            raise serializers.ValidationError(
                {'type': f'Tipo de notificación inválido. Opciones válidas: {", ".join(valid_types)}'}
            )
        
        if data.get('type') == 'form' and not data.get('form'):
            raise serializers.ValidationError(
                {'form': 'Este campo es requerido para notificaciones de tipo "form"'}
            )
        
        return data

    def validate_form(self, value):
        """Validación para evitar duplicados"""
        if value and Notification.objects.filter(form=value).exists():
            raise serializers.ValidationError(
                "Ya existe una notificación para este formulario"
            )
        return value

class MarkAsReadSerializer(serializers.Serializer):
    read = serializers.BooleanField(
        required=True,
        help_text="Indica si la notificación debe marcarse como leída (true) o no leída (false)"
    )

    def validate_read(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Debe ser un valor booleano")
        return value

    def update(self, instance, validated_data):
        read_status = validated_data.get('read', False)
        
        if read_status:
            instance.mark_as_read()
        else:
            instance.read = False
            instance.read_at = None
            instance.save()
            
        return instance