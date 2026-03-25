# --- Stage 1: The "Builder" ---
# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

FROM python:3.13-slim-bookworm AS builder
# This ONE line pulls the 'uv' binary and puts it in your image
# It is instant, no 'pip install' required!
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Even for Hello World, if SQLModel is in your uv.lock, you need these to BUILD
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV UV_PROJECT_ENVIRONMENT=/opt/venv
WORKDIR /build

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY ./src ./src
RUN uv sync --frozen --no-dev

# --- Stage 2: The "Runtime" ---
FROM python:3.13-slim-bookworm

# These are tiny and ensure that your DB connection works the moment you write the code
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

COPY --from=builder /opt/venv /opt/venv

WORKDIR /app
COPY ./src /app

# Ensure this path matches your folder structure!
COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

CMD ["/opt/run.sh"]