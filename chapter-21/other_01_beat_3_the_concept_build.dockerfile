# Dockerfile
FROM python:3.12-slim

# System dependencies for qiskit's C extensions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies first (cache-friendly layer ordering)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY quantum_service_async.py .
COPY quantum_cache.py .

# Non-root user for security
RUN useradd -m quantumuser
USER quantumuser

EXPOSE 8000

# Health check for orchestrators (K8s, ECS)
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "quantum_service_async:app", "--host", "0.0.0.0", "--port", "8000"]
