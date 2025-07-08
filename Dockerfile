# Use official Python image
FROM python:3.13.5-alpine

# Update system packages to reduce vulnerabilities
RUN apk update && apk upgrade && rm -rf /var/cache/apk/*

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app with uvicorn
CMD ["uvicorn", "rpp.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]