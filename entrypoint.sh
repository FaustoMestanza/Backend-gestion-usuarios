#!/bin/bash
set -e

echo " Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Verificando superusuario..."
python << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
cedula = "1719373001"
password = "Thomilia2302"
if not User.objects.filter(cedula=cedula).exists():
    print("Creando superusuario...")
    u = User.objects.create_superuser(
        cedula=cedula,
        username=cedula,
        password=password
    )
else:
    print("Superusuario ya existe, actualizando contraseña...")
    u = User.objects.get(cedula=cedula)
    u.set_password(password)
    u.save()
EOF

echo "Iniciando Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000
