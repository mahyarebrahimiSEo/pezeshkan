# Dockerfile - Lightweight, secure container for Pezeshkan Django Medical Architecture
FROM python:3.11-slim

# Install system dependencies for psycopg2 and Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-privileged user for security
RUN groupadd -g 1001 pezeshkan && \
    useradd -u 1001 -g pezeshkan -m -s /bin/bash pezeshkan

WORKDIR /app

# Copy application files
COPY --chown=pezeshkan:pezeshkan . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER pezeshkan

# Expose internal listening port
EXPOSE 3000

ENV ENVIRONMENT=production
ENV HOST=0.0.0.0
ENV PORT=3000
ENV PYTHONUNBUFFERED=1

# Run Django production server with high-concurrency Gunicorn + Uvicorn worker
CMD ["gunicorn", "config.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:3000", "--timeout", "60"]
