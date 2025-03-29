FROM python:3.11.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

ENV VIRTUAL_ENV=/code/.venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

# RUN useradd -m appuser && chown -R appuser:appuser /code
# USER appuser

# COPY --chown=appuser:appuser . .

EXPOSE 7860

# ENV PYTHONUNBUFFERED=1

CMD ["python", "api.py"]