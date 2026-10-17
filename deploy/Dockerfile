# Dockerfile - Lightweight, secure container for Pezeshkan Medical Server
FROM python:3.11-slim

# Create a non-privileged user for security
RUN groupadd -g 1001 pezeshkan && \
    useradd -u 1001 -g pezeshkan -m -s /bin/bash pezeshkan

WORKDIR /app

# Copy application files
COPY --chown=pezeshkan:pezeshkan . /app

# Install dependencies (argon2-cffi)
RUN pip install --no-cache-dir -r requirements.txt

# Switch to non-root user
USER pezeshkan

# Expose internal listening port
EXPOSE 3000

ENV ENVIRONMENT=production
ENV HOST=0.0.0.0
ENV PORT=3000

# Run with python unbuffered
CMD ["python", "-u", "server.py"]
