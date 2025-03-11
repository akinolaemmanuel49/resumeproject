# Use the latest syntax for Docker secrets
# syntax = docker/dockerfile:1.2

FROM python:3.11-slim

# Set environment variables (defaults for local dev)
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=resumeproject.settings

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/

# Install WeasyPrint dependencies and required system packages
RUN apt-get update && \
    apt-get install -y gcc libpq-dev \
    libpango-1.0-0 libpangoft2-1.0-0 gir1.2-harfbuzz-0.0 && \
    apt clean && \
    rm -rf /var/cache/apt/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . /app/

# 🔹 Inject secrets from Render’s `/etc/secrets/.env` during build
RUN --mount=type=secret,id=_env,dst=/etc/secrets/.env cat /etc/secrets/.env

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py makemigrations && python manage.py migrate

# Expose the port your app runs on
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "resumeproject.wsgi:application", "--workers=4"]
