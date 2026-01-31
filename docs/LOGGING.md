# Logging Configuration

## Overview

DataEngineX uses [structlog](https://www.structlog.org/) for structured, context-aware logging with automatic request ID tracking.

## Features

- **Structured JSON Logging**: Machine-parseable logs for production
- **Request ID Tracking**: Automatic UUID generation per request
- **Context Binding**: Request metadata (method, path, client) in all logs
- **Environment-based Configuration**: JSON (production) or console (dev) output
- **Middleware Integration**: Automatic request/response logging

## Configuration

### Environment Variables

- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) - default: INFO
- `LOG_FORMAT`: Output format (json, console) - default: json
- `ENVIRONMENT`: Environment name (dev, stage, prod) - default: dev

### Example

```bash
# Development - human-readable logs
export LOG_LEVEL=DEBUG
export LOG_FORMAT=console
export ENVIRONMENT=dev

# Production - JSON logs for aggregation
export LOG_LEVEL=INFO
export LOG_FORMAT=json
export ENVIRONMENT=prod
```

## Usage

### In Application Code

```python
import structlog

logger = structlog.get_logger(__name__)

# Simple logging
logger.info("user_action", user_id=123, action="login")

# With context binding
from structlog.contextvars import bind_contextvars

bind_contextvars(user_id=123, session_id="abc")
logger.info("processing_started")  # Includes user_id and session_id
```

### Request Context

Every HTTP request automatically gets:
- `request_id`: Unique UUID
- `method`: HTTP method (GET, POST, etc.)
- `path`: Request path
- `client_host`: Client IP address
- Response header: `X-Request-ID`

### Log Output Examples

**Development (Console):**
```
2026-01-30T16:30:45.123456Z [info     ] request_started method=GET path=/ request_id=123e4567-e89b-12d3-a456-426614174000
2026-01-30T16:30:45.234567Z [info     ] request_completed status_code=200 duration_seconds=0.111
```

**Production (JSON):**
```json
{
  "event": "request_started",
  "timestamp": "2026-01-30T16:30:45.123456Z",
  "level": "info",
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "method": "GET",
  "path": "/",
  "app": "dataenginex",
  "version": "0.1.0"
}
```

## Best Practices

1. **Use structured fields**: `logger.info("event_name", field1=value1)` not `logger.info(f"Event: {value1}")`
2. **Consistent event names**: Use snake_case, e.g., `user_login_success`
3. **Add context**: Use `bind_contextvars()` for request-scoped data
4. **Log levels**:
   - DEBUG: Detailed diagnostic info
   - INFO: General informational messages
   - WARNING: Warning messages for recoverable issues
   - ERROR: Error messages for failures
   - CRITICAL: Critical failures requiring immediate attention

## Testing

Run logging tests:
```bash
poetry run pytest tests/test_logging.py tests/test_middleware.py -v
```
