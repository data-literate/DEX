# Build stage
FROM python:3.11-slim AS builder

WORKDIR /build

# Install curl for uv installer
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency files
COPY pyproject.toml uv.lock Readme.md ./
COPY src/ src/

# Install dependencies to a virtual environment
ENV UV_PROJECT_ENVIRONMENT=/build/.venv \
    UV_PYTHON=/usr/local/bin/python \
    UV_PYTHON_PREFERENCE=system
RUN /root/.local/bin/uv sync --frozen --no-dev
FROM python:3.11-slim

WORKDIR /app

# Create non-root user
RUN groupadd --gid 1000 dex \
    && useradd --uid 1000 --gid dex --shell /bin/bash dex

# Copy virtual environment from builder
COPY --from=builder /build/.venv /app/.venv

# Copy application code
COPY src/ /app/src/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Switch to non-root user
USER dex

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI application
CMD ["python", "-m", "uvicorn", "dataenginex.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
