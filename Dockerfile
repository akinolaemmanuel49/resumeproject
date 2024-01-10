# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
# ENV PYTHONUNBUFFERED 1
# ENV DJANGO_SETTINGS_MODULE resumeproject.settings
# ENV SECRET_KEY "secret-key"

# Environment variables for email. Replace with appropriate values.
# ENV EMAIL_HOST "smtp.provider.com"
# ENV EMAIL_HOST_USER "example@mail.com"
# ENV EMAIL_HOST_PASSWORD "password"
# ENV EMAIL_PORT 587
# ENV EMAIL_USE_TLS True
# ENV DEFAULT_FROM_EMAIL "resumebuilder@resumebuilder.com"

# Create and set the working directory
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Collect static files
RUN python manage.py collectstatic --noinput
