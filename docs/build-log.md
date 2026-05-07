# Build Log

## Day 1 - Simple First, Production-Minded Always

I am building `ai-infra-starter-kit` because AI infrastructure is becoming part of normal software infrastructure, but the learning path often starts too late in the stack.

AI infra is intimidating because beginners are quickly surrounded by model serving frameworks, GPU scheduling, Kubernetes operators, distributed systems, observability, evals, and cost tradeoffs. Those topics matter, but they do not need to arrive all at once.

Simplicity is the edge for this project. The first version uses a small FastAPI service, structured logs, a metrics endpoint, Docker Compose, and an AI SRE Assistant that reads evidence. That is enough to teach the shape of the workflow without hiding the production direction.

Day 1 includes:

- `demo-service` with health, readiness, normal API, simulated errors, latency, memory pressure, logs, and metrics.
- `ai-sre-assistant` with API endpoints, CLI, rule-based analysis, and optional OpenAI-compatible LLM support.
- Docker Compose for local operation.
- Sample logs and questions.
- Docs for architecture, setup, observability, security, cost, and roadmap.

Next comes better observability: richer metrics, incident examples, dashboard basics, and clearer structured logging patterns.

