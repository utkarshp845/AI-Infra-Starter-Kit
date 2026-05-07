# Observability Basics

Observability starts with three questions:

- Is the service up?
- Is it doing the right work?
- When it fails, can we see enough evidence to debug it?

## Day 1 Signals

`demo-service` emits:

- Health via `/health`.
- Readiness via `/ready`.
- Structured logs for every request.
- Error logs for simulated failures.
- Warning logs for latency and memory pressure.
- Prometheus-style metrics via `/metrics`.

## What To Look For

- HTTP 5xx counts.
- Slow request durations.
- Repeated warning events.
- Missing or malformed structured fields.
- Differences between normal API paths and simulation paths.

The AI assistant is only useful when these signals are clear.

