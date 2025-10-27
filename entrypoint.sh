#!/bin/bash
echo "🚀 Ejecutando migraciones..."
python manage.py migrate --noinput

echo "📦 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "👑 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
u, _ = User.objects.get_or_create(cedula='1719373001', defaults={'username': '1719373001', 'is_staff': True, 'is_superuser': True});
u.set_password('Thomilia2302'); u.save();
print('✅ Superusuario creado o actualizado correctamente.');
"

echo "🔥 Iniciando Gunicorn..."
gunicorn project.wsgi:application --bind 0.0.0.0:8000
