# Pezeshkan Medical Ecosystem - Production Multi-Stage Dockerfile
FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=3000 \
    HOST=0.0.0.0

WORKDIR /app

# Install system dependencies for PostgreSQL, Pillow image processing, and compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Ensure data and upload directories exist
RUN mkdir -p /app/data /app/mag/uploads

EXPOSE 3000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:3000/api/pillars || exit 1

# Production server runner: Gunicorn with Uvicorn worker for maximum async throughput
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:3000", "--timeout", "60", "--access-logfile", "-"]
