from collections import Counter, defaultdict
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request, Response

from app.logging_config import logger
from app.routes import router


app = FastAPI(
    title="demo-service",
    description="A small production-shaped service for learning AI infrastructure basics.",
    version="0.1.0",
)

app.include_router(router)

REQUEST_TOTAL = Counter()
REQUEST_LATENCY_SECONDS = defaultdict(float)


@app.middleware("http")
async def record_requests(request: Request, call_next):
    request_id = request.headers.get("x-request-id", str(uuid4()))
    start = perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["x-request-id"] = request_id
        return response
    except Exception:
        logger.exception(
            "unhandled_request_error",
            extra={
                "event": "unhandled_request_error",
                "method": request.method,
                "path": request.url.path,
                "request_id": request_id,
            },
        )
        raise
    finally:
        duration_seconds = perf_counter() - start
        duration_ms = round(duration_seconds * 1000, 2)
        path = request.url.path

        REQUEST_TOTAL[(request.method, path, str(status_code))] += 1
        REQUEST_LATENCY_SECONDS[(request.method, path)] += duration_seconds

        logger.info(
            "request_completed",
            extra={
                "event": "request_completed",
                "method": request.method,
                "path": path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "request_id": request_id,
            },
        )


@app.get("/metrics")
def metrics() -> Response:
    lines = [
        "# HELP demo_service_requests_total Total HTTP requests handled by demo-service.",
        "# TYPE demo_service_requests_total counter",
    ]

    error_total = 0
    for (method, path, status), count in sorted(REQUEST_TOTAL.items()):
        if int(status) >= 500:
            error_total += count
        lines.append(
            f'demo_service_requests_total{{method="{method}",path="{path}",status="{status}"}} {count}'
        )

    lines.extend(
        [
            "# HELP demo_service_errors_total Total HTTP 5xx responses handled by demo-service.",
            "# TYPE demo_service_errors_total counter",
            f"demo_service_errors_total {error_total}",
            "# HELP demo_service_request_latency_seconds_sum Total request latency by method and path.",
            "# TYPE demo_service_request_latency_seconds_sum counter",
        ]
    )

    for (method, path), seconds in sorted(REQUEST_LATENCY_SECONDS.items()):
        lines.append(
            f'demo_service_request_latency_seconds_sum{{method="{method}",path="{path}"}} {seconds:.6f}'
        )

    return Response(content="\n".join(lines) + "\n", media_type="text/plain")

