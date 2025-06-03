# --- Stage 1: Build ---
FROM python:alpine AS builder

RUN apk add --no-cache build-base

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./

RUN uv pip install --prefix=/install --no-cache

COPY ./src ./src

# --- Stage 2: Runtime ---
FROM python:alpine

WORKDIR /app


COPY --from=builder /install /usr/local

COPY --from=builder /app/src ./src


CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
