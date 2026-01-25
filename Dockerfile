# Build stage
FROM python:3.11-slim AS builder

WORKDIR /build

# Install poetry
RUN pip install --no-cache-dir poetry==2.3.0

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies to a virtual environment
RUN poetry config virtualenvs.in-project true && \
    poetry install --no-dev --no-interaction --no-ansi

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /build/.venv /app/.venv

# Copy application code
COPY src/ /app/src/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose FastAPI default port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "dataenginex.main:app", "--host", "0.0.0.0", "--port", "8000"]
