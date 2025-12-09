# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY weather_agent.py .
COPY app.py .

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Expose port (Cloud Run will set PORT environment variable)
EXPOSE 8080

# Run with gunicorn for production
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
