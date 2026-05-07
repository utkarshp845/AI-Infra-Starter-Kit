# Cost Optimization

AI infrastructure cost is usually driven by model choice, request volume, latency targets, context size, and hardware utilization.

Day 1 cost controls:

- No GPU required.
- LLM usage is optional.
- Rule-based analysis works offline.
- Log context is capped by `max_lines`.

Future cost topics:

- Smaller models for routine analysis.
- Caching repeated incident summaries.
- Token budgets.
- Batch analysis.
- GPU utilization.
- Autoscaling and scale-to-zero patterns.

