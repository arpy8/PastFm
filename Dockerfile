FROM python:3.11-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip uv

# Copy requirements file separately to leverage Docker cache
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

# Create non-root user
RUN useradd -m appuser 
RUN mkdir -p /app/logs /app/static && \
    chown -R appuser:appuser /app
USER appuser

# Copy application code
COPY --chown=appuser:appuser . .

# Expose the application port
EXPOSE 7860

# Command to run the application
CMD ["python", "main.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/health || exit 1