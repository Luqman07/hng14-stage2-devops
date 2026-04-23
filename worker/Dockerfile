# ── Stage 1: build ─────────────────────────────────────────
FROM python:3.12-alpine AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime ───────────────────────────────────────
FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local

COPY . .

RUN adduser --no-create-home --disabled-password appuser \
    && chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import redis,os; r=redis.Redis(host=os.environ['REDIS_HOST'],port=int(os.environ.get('REDIS_PORT',6379)),password=os.environ['REDIS_PASSWORD']); r.ping()"

CMD ["python", "worker.py"]
