# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Rol

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "descripcion")
    search_fields = ("nombre",)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "cedula", "username", "rol", "curso", "is_active", "is_staff")
    search_fields = ("cedula", "username", "first_name", "last_name", "curso")
    list_filter = ("rol", "is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("cedula", "password")}),
        ("Información personal", {"fields": ("username", "first_name", "last_name", "email", "rol", "curso")}),
        ("Permisos", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Fechas importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("cedula", "username", "password1", "password2", "rol", "curso", "is_staff", "is_active"),
        }),
    )
