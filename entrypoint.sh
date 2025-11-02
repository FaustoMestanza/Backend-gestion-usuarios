#!/bin/bash
set -e

<<<<<<< HEAD
echo "🚀 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
=======
echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo " Recolectando archivos estáticos..."
>>>>>>> ac3c381 (Agrego pruebas unitarias y funcionales + configuración CI/CD en GitHub Actions)
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

<<<<<<< HEAD
print('✅ Superusuario creado o actualizado correctamente.' if created else '🔁 Superusuario ya existía y fue actualizado.')
=======
print('Superusuario creado o actualizado correctamente.' if created else '🔁 Superusuario ya existía y fue actualizado.')
>>>>>>> ac3c381 (Agrego pruebas unitarias y funcionales + configuración CI/CD en GitHub Actions)
EOF

echo "🔥 Iniciando Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000
