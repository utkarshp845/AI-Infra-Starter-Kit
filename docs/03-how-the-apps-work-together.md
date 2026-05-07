# How The Apps Work Together

The connection between the apps is a shared log file.

1. `demo-service` receives requests.
2. It writes structured JSON logs to stdout and to `DEMO_SERVICE_LOG_PATH`.
3. Docker Compose mounts `./logs` into both containers.
4. `ai-sre-assistant` reads the recent log lines.
5. The analyzer extracts errors, warnings, slow requests, and evidence.
6. The API or CLI returns a concise operational summary.

## Why File Logs First

File logs are not the final production design, but they are useful for learning:

- They are visible.
- They are easy to inspect.
- They do not require a logging backend.
- They make the evidence path obvious.

Later versions can replace the file path with OpenTelemetry, Loki, Elasticsearch, CloudWatch, or another logging backend.

