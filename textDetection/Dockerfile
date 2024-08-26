# Stage 1: Build the application
FROM python:3.10-slim AS build

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
# Expose port 80 for internal communication
EXPOSE 80

# Start Django application using Gunicorn
CMD ["gunicorn", "textDetection.wsgi:application", "--bind", "0.0.0.0:80"]
