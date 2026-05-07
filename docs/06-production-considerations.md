# Production Considerations

Day 1 is local and simple. Production adds constraints.

## Logging

A shared file is useful locally, but production should use a real log pipeline. Options include OpenTelemetry collectors, Loki, Elasticsearch, CloudWatch, or a managed observability platform.

## Health And Readiness

Health checks should answer whether the process is alive. Readiness checks should answer whether the service can safely receive traffic.

## Reliability

Before adding advanced model serving, define:

- SLOs.
- Error budgets.
- Alert thresholds.
- Rollback paths.
- Incident review habits.

## Advanced Serving Comes Later

Tools such as vLLM, Triton, Ray, and KServe are valuable when the project reaches model serving scale. They are roadmap items, not Day 1 requirements.

