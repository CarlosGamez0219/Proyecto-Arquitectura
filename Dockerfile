# Usamos una imagen ligera de Python
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /app/

# Recolectar archivos estáticos
RUN python manage.py collectstatic --noinput

# Servidor de producción
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]