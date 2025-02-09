# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE resumeproject.settings
ENV SECRET_KEY "secret-key"

# Environment variables for email. Replace with appropriate values.
ENV EMAIL_HOST "smtp.provider.com"
ENV EMAIL_HOST_USER "example@mail.com"
ENV EMAIL_HOST_PASSWORD "password"
ENV EMAIL_PORT 587
ENV EMAIL_USE_TLS True
ENV DEFAULT_FROM_EMAIL "resumebuilder@resumebuilder.com"

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install WeasyPrint dependencies
# for building packages that have native extensions and then weasyprint dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev \
    libpango-1.0-0 libpangoft2-1.0-0 gir1.2-harfbuzz-0.0 && \
    apt clean && \
    rm -rf /var/cache/apt/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run Django's development server
RUN python manage.py makemigrations && python manage.py migrate
CMD ["python", "manage.py", "runserver"]

# Collect static files
RUN python manage.py collectstatic --noinput
