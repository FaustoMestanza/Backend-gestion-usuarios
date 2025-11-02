# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


class Rol(models.Model):
    nombre = models.CharField(max_length=30, unique=True)   # "DOCENTE", "ESTUDIANTE", "DIRECTOR", "ADMIN"
    descripcion = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.nombre


class User(AbstractUser):
    cedula = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        validators=[RegexValidator(r'^\d{10}$', 'La cédula debe tener 10 dígitos.')]
    )
    # Solo aplica a estudiantes. 
    curso = models.CharField(max_length=50, null=True, blank=True)

    # FK a Rol 
    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name="usuarios",
         null=True,
        blank=True
        
    )

    # Usar cédula para autenticación
    USERNAME_FIELD = "cedula"
    REQUIRED_FIELDS = ["username"]  # para createsuperuser

    # Reglas de negocio
    def clean(self):
        super().clean()
        # Si aún no hay rol (caso createsuperuser), no validar nada más
        if not self.rol:
            return
        # Si tiene rol y NO es ESTUDIANTE, curso debe estar vacío
        if self.rol.nombre != "ESTUDIANTE" and self.curso:
            raise ValidationError({"curso": "El curso solo aplica a usuarios con rol ESTUDIANTE."})

    # Garantiza que clean() se ejecute siempre
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
