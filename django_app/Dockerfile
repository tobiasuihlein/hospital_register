# Use official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /hospital_register_app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmysqlclient-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current project files to the container
COPY . /hospital_register_app

# Collect static files
RUN python manage.py collectstatic --noinput

# Set environment variables to improve Python performance
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Expose port 8000 for Django app (optional)
EXPOSE 8000

# Run the application (using Gunicorn for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "my_project.wsgi:application"]
