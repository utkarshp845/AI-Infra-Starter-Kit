# AI SRE Assistant Design

The assistant is intentionally evidence-grounded.

System prompt:

```text
You are an AI SRE assistant. Your job is to analyze logs and symptoms, identify likely causes, suggest safe debugging steps, and avoid pretending to know things not present in the evidence.
```

## Behavior

The assistant should:

- Cite log lines or events when possible.
- Separate facts from guesses.
- Avoid dangerous commands.
- Recommend safe next steps.
- Be concise and practical.

## Fallback Mode

LLM access should not be required to learn the workflow. The rule-based analyzer:

- Counts errors, warnings, and slow events.
- Extracts endpoint and status patterns.
- Identifies intentional simulation endpoints.
- Suggests safe debugging steps.

If an LLM provider is configured, the LLM receives the rule-based analysis plus recent log evidence.

## Metrics Analysis

The assistant can also read `demo-service` metrics.

By default it fetches:

```text
DEMO_SERVICE_METRICS_URL=http://demo-service:8000/metrics
```

The metrics analyzer stays deterministic and dependency-free. It looks for:

- Total HTTP requests.
- HTTP 5xx responses.
- Top paths by request count.
- Simulated error events.
- Simulated latency events.
- Memory pressure events.
- Basic latency hints from histogram buckets.

This adds a second evidence source.

Logs answer what happened in specific events. Metrics answer how often and where the symptoms appeared.

## Combined Incident Summary

`POST /summarize-incident` now includes:

- Log analysis.
- Metrics analysis.
- Combined interpretation.

The intended pattern is:

```text
Signals -> Evidence -> Analysis -> Safe next steps
```

The assistant should not replace observability. It should explain the evidence already emitted by the service.
