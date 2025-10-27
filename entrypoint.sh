#!/bin/bash
# entrypoint.sh
set -e  # Detiene la ejecución si algún comando falla

# ---------------------------------------------
# 1️Aplicar migraciones antes de levantar el servidor
# ---------------------------------------------
echo " Ejecutando migraciones..."
python manage.py migrate --noinput

# ---------------------------------------------
#  Recolectar archivos estáticos
# ---------------------------------------------
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# ---------------------------------------------
# Crear superusuario automáticamente (si no existe)
# ---------------------------------------------
if [ "$DJANGO_SUPERUSER_CEDULA" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creando superusuario por defecto (si no existe)..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
cedula = "${DJANGO_SUPERUSER_CEDULA}"
password = "${DJANGO_SUPERUSER_PASSWORD}"
if not User.objects.filter(cedula=cedula).exists():
    User.objects.create_superuser(
        cedula=cedula,
        password=password,
        first_name="Admin",
        last_name="Principal"
    )
    print(f"Superusuario creado correctamente con cédula {cedula}")
else:
    print(f"El superusuario con cédula {cedula} ya existe, no se crea otro.")
END
fi

# ---------------------------------------------
# 4️⃣ Arrancar Gunicorn
# ---------------------------------------------
echo "Iniciando Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 3
