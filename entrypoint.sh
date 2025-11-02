#!/bin/bash
set -e

echo "🚀 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "👑 Verificando superusuario..."
python manage.py shell <<EOF
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()

u, created = User.objects.get_or_create(
    cedula='1719373001',
    defaults={
        'username': '1719373001',
        'is_staff': True,
        'is_superuser': True
    }
)
u.set_password('Thomilia2302')
u.save()

print('✅ Superusuario creado o actualizado correctamente.' if created else '🔁 Superusuario ya existía y fue actualizado.')
EOF

echo "🔥 Iniciando Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000
