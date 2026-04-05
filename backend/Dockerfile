# Use slim Python image
FROM python:3.11-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some tools)
RUN apt-get update && apt-get install -y \
    build-essential \
    nmap \
    dnsutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install websockets

# Copy the rest of the app
COPY . .

# Expose API port
EXPOSE 8000

# Default command (API)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]