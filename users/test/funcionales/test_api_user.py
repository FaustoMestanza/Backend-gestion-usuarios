# users/tests/funcionales/test_api_user.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Rol

class UserAPITest(APITestCase):
    def setUp(self):
        self.rol = Rol.objects.create(nombre="DOCENTE")
        self.url = reverse('user-list')  # según tu router
        self.data = {
            "username": "fausto",
            "cedula": "1234567890",
            "rol": self.rol.id,
        }

    def test_crear_usuario(self):
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_listar_usuarios(self):
        User.objects.create(username="test", cedula="1111111111", rol=self.rol)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
