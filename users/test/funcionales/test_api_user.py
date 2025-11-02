# users/tests/funcionales/test_api_user.py
# users/test/funcionales/test_api_user.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Rol


class UserAPITest(APITestCase):
    """Pruebas funcionales del API de usuarios (sin modificar serializer)"""

    def setUp(self):
        self.rol = Rol.objects.create(nombre="DOCENTE")
        self.url = reverse('usuario-list')

        # Creamos usuario directamente en DB (no vía serializer)
        self.user = User.objects.create_user(
            username="fausto",
            cedula="1234567890",
            password="12345",
            rol=self.rol
        )

    def test_listar_usuarios(self):
        """Debe listar los usuarios registrados"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertIn("username", response.data[0])

    def test_crear_usuario_devuelve_error_por_campo_rol(self):
        """Debe devolver error 400 al intentar crear usuario (por serializer)"""
        data = {
            "username": "nuevo",
            "password": "12345",
            "cedula": "1111111111",
            "rol": self.rol.nombre  # no soportado en create
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
