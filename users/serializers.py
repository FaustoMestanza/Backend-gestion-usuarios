# users/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(serializers.ModelSerializer):
    # Con opción B (Rol como entidad), exponemos el nombre del rol
    rol = serializers.CharField(source="rol.nombre")

    class Meta:
        model = User
        fields = ("id", "cedula", "username", "first_name", "last_name", "rol", "curso")

class LoginSerializer(TokenObtainPairSerializer):
    """
    Valida cedula + password (USERNAME_FIELD = 'cedula')
    Devuelve tokens y adjunta el usuario serializado.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["rol"] = user.rol.nombre if user.rol else None  # claim opcional
        return token

    def validate(self, attrs):
        data = super().validate(attrs)   # genera access/refresh
        data["user"] = UserSerializer(self.user).data
        return data
