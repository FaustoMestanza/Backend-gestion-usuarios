# users/tests/funcionales/test_api_user.py
# users/test/funcionales/test_api_user.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Rol


class UserAPITest(APITestCase):
    """Pruebas funcionales del API de usuarios"""

    def setUp(self):
        # Crear un rol de ejemplo
        self.rol = Rol.objects.create(nombre="DOCENTE")
        # URL generada automáticamente por el router (basename='usuario')
        self.url = reverse('usuario-list')

        # Datos de ejemplo para crear usuario
        self.data = {
            "username": "fausto",
            "password": "12345",
            "cedula": "1234567890",
            "rol": self.rol.id,
        }

    def test_crear_usuario(self):
        """Debe crear un usuario exitosamente vía API"""
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_listar_usuarios(self):
        """Debe listar los usuarios registrados"""
        User.objects.create_user(
            username="test",
            cedula="1111111111",
            password="12345",
            rol=self.rol
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
