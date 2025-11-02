# users/tests/unitarias/test_models_user.py
# users/test/unitarias/test_models_user.py
from django.test import TestCase
from users.models import User, Rol
from django.core.exceptions import ValidationError


class RolModelTest(TestCase):
    """Pruebas unitarias del modelo Rol"""

    def test_creacion_rol(self):
        rol = Rol.objects.create(nombre="DOCENTE", descripcion="Rol docente")
        self.assertEqual(str(rol), "DOCENTE")
        self.assertEqual(rol.descripcion, "Rol docente")


class UserModelTest(TestCase):
    """Pruebas unitarias del modelo User"""

    def setUp(self):
        self.rol_estudiante = Rol.objects.create(nombre="ESTUDIANTE")
        self.rol_docente = Rol.objects.create(nombre="DOCENTE")

    def test_crear_usuario_estudiante_con_curso(self):
        """Un estudiante puede tener curso asignado"""
        usuario = User.objects.create_user(
            username="test1",
            password="12345",
            cedula="1234567890",
            rol=self.rol_estudiante,
            curso="10mo A"
        )
        self.assertEqual(usuario.curso, "10mo A")

    def test_error_usuario_docente_con_curso(self):
        """Un docente no puede tener curso asignado"""
        usuario = User(
            username="test2",
            password="12345",
            cedula="0987654321",
            rol=self.rol_docente,
            curso="10mo B"
        )
        with self.assertRaises(ValidationError):
            usuario.full_clean()
