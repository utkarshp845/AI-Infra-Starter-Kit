# demo-service

`demo-service` is a small FastAPI application that behaves like a production service on purpose. It has health checks, normal API endpoints, simulated errors, simulated latency, memory pressure, structured JSON logs, and a Prometheus-style metrics endpoint.

The service exists so the AI SRE Assistant has real signals to inspect.

## Run Locally

From the repository root:

```bash
make up
make generate-traffic
```

Open:

- `GET http://localhost:8000/health`
- `GET http://localhost:8000/ready`
- `GET http://localhost:8000/api/orders`
- `GET http://localhost:8000/simulate/error`
- `GET http://localhost:8000/simulate/latency`
- `GET http://localhost:8000/simulate/memory-pressure`
- `GET http://localhost:8000/metrics`

## Logs

The app writes JSON logs to stdout and to `DEMO_SERVICE_LOG_PATH`.

In Docker Compose, that path is:

```text
/shared/logs/demo-service.log
```

On the host, it appears at:

```text
./logs/demo-service.log
```

