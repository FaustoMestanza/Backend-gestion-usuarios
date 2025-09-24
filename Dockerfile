# Dockerfile
FROM python:3.12-slim

# Evita .pyc y hace logging inmediato
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Carpeta de trabajo
WORKDIR /app

# Dependencias del sistema (mínimas)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala requirements primero (aprovecha caché)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el proyecto
COPY . .

# Exponer puerto de desarrollo
EXPOSE 8000

# Comando por defecto (dev)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
