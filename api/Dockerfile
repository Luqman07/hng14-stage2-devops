# ── Stage 1: build ──────────────────────────────────────────
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime ────────────────────────────────────────
FROM python:3.12-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Copy installed packages
COPY --from=builder /install /usr/local

# Copy application source
COPY main.py .

# Create non-root user
RUN adduser --no-create-home --disabled-password appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
CMD python -c "import urllib.request,sys; \
sys.exit(0) if urllib.request.urlopen('http://localhost:8000/health').getcode()==200 else sys.exit(1)"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]