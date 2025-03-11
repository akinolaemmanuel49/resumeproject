# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set non-sensitive environment variables
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=resumeproject.settings

# Set the working directory
WORKDIR /app

# Copy the requirements file first (optimizing Docker cache layers)
COPY requirements.txt /app/

# Install system dependencies (for WeasyPrint and database support)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev \
    libpango-1.0-0 libpangoft2-1.0-0 gir1.2-harfbuzz-0.0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose Render's dynamically assigned port
EXPOSE $PORT

# Load secrets from Render's Secret Files and start the server
CMD ["sh", "-c", "
    if [ -f /etc/secrets/.env ]; then
        export \$(grep -v '^#' /etc/secrets/.env | xargs);
    fi &&
    python manage.py collectstatic --noinput &&
    python manage.py migrate &&
    exec gunicorn --bind 0.0.0.0:$PORT resumeproject.wsgi:application --workers=4
"]
