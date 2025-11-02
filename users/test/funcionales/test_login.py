# users/tests/unitarias/test_models_user.py
# users/test/funcionales/test_login.py
from django.test import TestCase
from users.models import User, Rol
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse


class LoginAPITest(TestCase):
    """Pruebas funcionales del login y autenticación"""

    def setUp(self):
        self.client = APIClient()
        self.rol = Rol.objects.create(nombre="DOCENTE")
        self.user = User.objects.create_user(
            username="fausto",
            cedula="1234567890",
            password="12345",
            rol=self.rol
        )
        self.login_url = reverse('auth-login')

    def test_login_correcto(self):
        """Debe autenticar correctamente al usuario"""
        data = {"cedula": "1234567890", "password": "12345"}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_incorrecto(self):
        """Debe fallar si las credenciales son incorrectas"""
        data = {"cedula": "9999999999", "password": "wrong"}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
