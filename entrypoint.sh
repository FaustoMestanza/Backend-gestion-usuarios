#!/bin/bash
# ===========================================
# entrypoint.sh — Django en Azure App Service
# ===========================================
set -e  # Detiene el script si ocurre un error

echo "🔹 Iniciando despliegue Django..."

# 1️⃣ Aplicar migraciones antes de levantar el servidor
echo "🔹 Ejecutando migraciones..."
python manage.py migrate --noinput

# 2️⃣ Recolectar archivos estáticos
echo "🔹 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# 3️⃣ Crear o actualizar superusuario automáticamente
echo "🔹 Verificando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
cedula = '1719373001';
password = 'Thomilia2302';
username = '1719373001';
try:
    if not User.objects.filter(cedula=cedula).exists():
        User.objects.create_superuser(cedula=cedula, username=username, password=password);
        print('✅ Superusuario creado correctamente.');
    else:
        u = User.objects.get(cedula=cedula);
        u.set_password(password);
        u.save();
        print('🔄 Contraseña del superusuario actualizada.');
except Exception as e:
    print('⚠️ Error al crear o actualizar el superusuario:', e)
"

# 4️⃣ Iniciar Gunicorn (servidor de Django)
echo "🚀 Iniciando Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000

