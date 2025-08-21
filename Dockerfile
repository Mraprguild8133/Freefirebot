FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Try installing with uv first, fall back to pip if it fails
COPY requirements.txt ./
RUN pip install --no-cache-dir uv && \
    (uv pip install --no-cache -r requirements.txt || \
     pip install --no-cache-dir -r requirements.txt)

COPY . .

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    procps \
    htop \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
    
# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER firebot

# Expose ports
EXPOSE 5000 8080

# Set process priority and start application
CMD ["nice", "-n", "0", "python", "process_manager.py"]
