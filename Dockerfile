FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
    
# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Switch to non-root user
USER firebot

# Expose ports
EXPOSE 5000 8080

# Set process priority and start application
CMD ["nice", "-n", "0", "python", "process_manager.py"]
