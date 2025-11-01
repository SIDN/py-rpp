# Use official Python image
FROM python:3.13-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install build dependencies, then remove them after pip install
RUN apk update && \
    apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev && \
    apk add --no-cache libpq && \
    rm -rf /var/cache/apk/*

# Copy only requirements first for better cache usage
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps

# Copy application code
COPY . .

# Create a non-root user and switch to it
RUN adduser -D appuser
USER appuser

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app with Gunicorn and Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "rpp.main:app", "--bind", "0.0.0.0:8000"]