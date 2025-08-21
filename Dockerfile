# Free Fire Telegram Bot Docker Image
# Multi-stage build for optimized production deployment

# Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY pyproject.toml uv.lock ./
RUN pip install uv && \
    uv pip install --system -r uv.lock

# Production stage
FROM python:3.11-slim as production

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

# Create non-root user for security
RUN groupadd -r firebot && useradd -r -g firebot firebot

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create app directory and set permissions
WORKDIR /app
RUN chown -R firebot:firebot /app

# Copy application code
COPY --chown=firebot:firebot . .

# Set resource limits and priority
# CPU: Mean priority (nice value 0)
# Memory: 512MB limit
# Network: Standard priority
RUN echo "firebot soft cpu 2" >> /etc/security/limits.conf && \
    echo "firebot hard cpu 4" >> /etc/security/limits.conf && \
    echo "firebot soft memlock 536870912" >> /etc/security/limits.conf && \
    echo "firebot hard memlock 536870912" >> /etc/security/limits.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER firebot

# Expose ports
EXPOSE 5000 8080

# Set process priority and start application
CMD ["nice", "-n", "0", "python", "process_manager.py"]