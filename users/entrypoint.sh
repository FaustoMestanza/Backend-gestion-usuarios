#!/bin/bash
# entrypoint.sh
set -e  # Detener ejecución si algún comando falla

# Aplicar migraciones antes de levantar el servidor
echo "📦 Ejecutando migraciones..."
python manage.py migrate --noinput

# Colectar estáticos (por si acaso)
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Crear superusuario automáticamente (si no existe)
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
    echo "Creando superusuario por defecto..."
    python manage.py createsuperuser \
        --noinput \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

# Arrancar Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn project.wsgi:application --bind 0.0.0.0:8000
