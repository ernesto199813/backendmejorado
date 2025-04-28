from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser
from django.db import IntegrityError  # ✅ Import necesario

# --- Serializador para el Token Personalizado ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        """
        Personaliza el token JWT para incluir información adicional.
        """
        token = super().get_token(user)

        # Agregar claims personalizados al token
        token['username'] = user.username
        token['email'] = user.email
        if hasattr(user, 'role'):
            token['role'] = user.role

        return token

    def validate(self, attrs):
        """
        Personaliza la respuesta del token para incluir datos adicionales.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
        }
        if hasattr(self.user, 'role'):
            data['user']['role'] = self.user.role

        return data

# --- Serializador para el Modelo de Usuario (con hasheo de contraseña) ---
class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo CustomUser, maneja la creación y visualización.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        try:
            user = CustomUser.objects.create_user(
                password=password,
                **validated_data
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError({
                "detail": "Ya existe un usuario con este nombre de usuario o correo electrónico."
            })
