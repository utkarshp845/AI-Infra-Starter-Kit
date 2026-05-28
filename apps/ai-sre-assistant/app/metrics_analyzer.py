from collections import Counter, defaultdict
from typing import Any

from app.metrics_reader import MetricSample


def analyze_metrics(samples: list[MetricSample], source: str | None = None) -> dict[str, Any]:
    if not samples:
        return {
            "summary": "No demo-service metrics were available.",
            "source": source,
            "facts": ["No parseable Prometheus metric samples were found."],
            "signals": {
                "total_requests": 0,
                "http_5xx": 0,
                "simulated_errors": 0,
                "simulated_latency_events": 0,
                "memory_pressure_events": 0,
            },
            "top_paths": [],
            "latency_hints": [],
            "next_steps": [
                "Check that demo-service is running.",
                "Check that DEMO_SERVICE_METRICS_URL points to the demo-service /metrics endpoint.",
                "Generate traffic before asking for metrics analysis.",
            ],
        }

    http_requests = [sample for sample in samples if sample.name == "demo_service_http_requests_total"]
    total_requests = int(sum(sample.value for sample in http_requests))
    http_5xx = int(
        sum(sample.value for sample in http_requests if sample.labels.get("status_code", "").startswith("5"))
    )
    status_counts = Counter()
    path_counts = Counter()

    for sample in http_requests:
        status_counts[sample.labels.get("status_code", "unknown")] += int(sample.value)
        path_counts[sample.labels.get("path", "unknown")] += int(sample.value)

    simulated_errors = _sum_metric(samples, "demo_service_simulated_errors_total")
    simulated_latency_events = _sum_metric(samples, "demo_service_simulated_latency_events_total")
    memory_pressure_events = _sum_metric(samples, "demo_service_memory_pressure_events_total")
    latency_hints = _latency_hints(samples)

    facts = [
        f"Total HTTP requests observed in metrics: {total_requests}.",
        f"HTTP 5xx responses observed in metrics: {http_5xx}.",
        f"Simulated error events: {simulated_errors}.",
        f"Simulated latency events: {simulated_latency_events}.",
        f"Memory pressure events: {memory_pressure_events}.",
    ]
    if status_counts:
        facts.append(f"HTTP status counts from metrics: {dict(status_counts)}.")
    if path_counts:
        facts.append(f"Most active path from metrics: {path_counts.most_common(1)[0][0]}.")

    next_steps = [
        "Compare metrics evidence with recent structured logs.",
        "Check whether unhealthy signals are isolated to simulation endpoints.",
        "Use request IDs in logs to inspect specific failures.",
    ]
    if http_5xx:
        next_steps.append("Inspect recent logs for ERROR events and HTTP 500 request_completed entries.")
    if simulated_latency_events:
        next_steps.append("Compare latency bucket hints with /simulate/latency request logs.")
    if memory_pressure_events:
        next_steps.append("Check memory pressure log entries before assuming a memory leak.")

    return {
        "summary": _summary(
            total_requests=total_requests,
            http_5xx=http_5xx,
            simulated_errors=simulated_errors,
            simulated_latency_events=simulated_latency_events,
            memory_pressure_events=memory_pressure_events,
        ),
        "source": source,
        "facts": facts,
        "signals": {
            "total_requests": total_requests,
            "http_5xx": http_5xx,
            "simulated_errors": simulated_errors,
            "simulated_latency_events": simulated_latency_events,
            "memory_pressure_events": memory_pressure_events,
            "status_counts": dict(status_counts),
        },
        "top_paths": [{"path": path, "requests": count} for path, count in path_counts.most_common(5)],
        "latency_hints": latency_hints,
        "next_steps": next_steps,
    }


def combined_incident_analysis(log_analysis: dict[str, Any], metrics_analysis: dict[str, Any]) -> dict[str, Any]:
    metrics_signals = metrics_analysis.get("signals", {})
    log_summary = log_analysis.get("summary", "No log summary available.")
    metrics_summary = metrics_analysis.get("summary", "No metrics summary available.")

    facts = [
        f"Log summary: {log_summary}",
        f"Metrics summary: {metrics_summary}",
    ]
    guesses = []

    if metrics_signals.get("http_5xx", 0) and "simulate/error" in str(log_analysis):
        guesses.append("Errors appear to be isolated to the intentional /simulate/error endpoint.")
    if metrics_signals.get("simulated_latency_events", 0) and "simulate/latency" in str(log_analysis):
        guesses.append("Latency appears connected to intentional /simulate/latency traffic.")
    if metrics_signals.get("memory_pressure_events", 0) and "memory" in str(log_analysis).lower():
        guesses.append("Memory pressure appears connected to intentional /simulate/memory-pressure traffic.")
    if not guesses:
        guesses.append("Use the log and metrics sections together before choosing a root cause.")

    return {
        "summary": "Combined incident analysis includes both recent logs and demo-service metrics.",
        "facts": facts,
        "guesses": guesses,
        "next_steps": [
            "Start with metric signals to identify the affected path or symptom.",
            "Use log evidence and request IDs to inspect concrete examples.",
            "Prefer the safest simulation-specific explanation when evidence points to simulation endpoints.",
        ],
    }


def _sum_metric(samples: list[MetricSample], name: str) -> int:
    return int(sum(sample.value for sample in samples if sample.name == name))


def _latency_hints(samples: list[MetricSample]) -> list[str]:
    counts_by_route: dict[tuple[str, str], int] = {}
    under_one_second_by_route: defaultdict[tuple[str, str], int] = defaultdict(int)

    for sample in samples:
        if sample.name == "demo_service_http_request_duration_seconds_count":
            key = (sample.labels.get("method", "unknown"), sample.labels.get("path", "unknown"))
            counts_by_route[key] = int(sample.value)
        if sample.name == "demo_service_http_request_duration_seconds_bucket" and sample.labels.get("le") == "1":
            key = (sample.labels.get("method", "unknown"), sample.labels.get("path", "unknown"))
            under_one_second_by_route[key] = int(sample.value)

    hints = []
    for (method, path), total in sorted(counts_by_route.items()):
        over_one_second = total - under_one_second_by_route[(method, path)]
        if over_one_second > 0:
            hints.append(f"{over_one_second} {method} request(s) to {path} exceeded 1 second.")

    return hints


def _summary(
    total_requests: int,
    http_5xx: int,
    simulated_errors: int,
    simulated_latency_events: int,
    memory_pressure_events: int,
) -> str:
    if total_requests == 0:
        return "Metrics are available, but no HTTP requests have been recorded yet."

    return (
        f"Metrics show {total_requests} request(s), {http_5xx} HTTP 5xx response(s), "
        f"{simulated_errors} simulated error event(s), {simulated_latency_events} simulated latency event(s), "
        f"and {memory_pressure_events} memory pressure event(s)."
    )
