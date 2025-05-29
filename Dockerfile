FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser 
RUN mkdir -p /app/logs /app/static && \
    chown -R appuser:appuser /app
USER appuser

COPY --chown=appuser:appuser . .

RUN if [ ! -f /app/static/temp.gif ]; then \
    touch /app/static/temp.gif; \
    fi

EXPOSE 7860

CMD ["python", "main.py"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:7860/health || exit 1