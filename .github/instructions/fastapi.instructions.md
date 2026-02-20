---
applyTo: "src/**/api/**/*.py"
---

# FastAPI — Project Specifics

## Routing & Responses
- Versioned routes: `APIRouter(prefix="/api/v1", tags=["v1"])`
- Declare `response_model=` on every endpoint
- Pydantic models for all request/response shapes
- Custom `custom_openapi()` in main.py for schema customization

## Lifespan & Middleware
- `@asynccontextmanager` lifespan for startup/shutdown
- Middleware stack (order matters): request logging → metrics → auth → rate limit
- Uses `BaseHTTPMiddleware` (not `Depends()`) — keeps cross-cutting logic out of route signatures
- 3 global exception handlers: `RequestValidationError`, `StarletteHTTPException`, catch-all `Exception`
- Lazy imports inside route handlers (e.g., `PipelineConfig`) to avoid circular deps

## Project Map
- Entry: `src/careerdex/api/main.py` (logging + tracing configured at module level)
- Auth: `auth.py` — pure-Python HS256 JWT (no pyjwt dependency)
- Health: `health.py` — TCP checks for DB, cache, external API
- Routers: `routers/v1.py` | Pagination: `pagination.py` (cursor-based, base64 opaque cursors)
- Rate limiting: `rate_limit.py` (token-bucket) | Errors: `errors.py`
- Metrics: `middleware/metrics.py` (`http_requests_total`, `http_request_duration_seconds`)

## Local Dev
- `poe dev` → uvicorn on port 8000 with reload
- Docs: `http://localhost:8000/docs`
- Bruno collection: `api-collection/`
