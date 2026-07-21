# Roadmap

This is the canonical technical execution order for AIOps Lab. Weeks 1-4 are the completed learning foundation, Weeks 5-8 are the next measurement cycle, and later infrastructure remains gated by evidence and named operational ownership.

## Week 1 - Local Learning Lab

- Local demo-service.
- AI SRE Assistant.
- Docker Compose.
- Sample logs.
- Basic README.

## Week 2 - Observability Basics

- Metrics improvements.
- Structured logging refinements.
- Request correlation.
- Incident examples.
- Assistant metrics analysis.

## Week 3 - Kubernetes Foundations

- kind-first Kubernetes manifests.
- Operations runbook.
- ConfigMaps and Secrets.
- Health checks and resource limits.
- Incident debugging walkthrough.
- Production next-steps guide.

## Week 4 - Production Readiness

- Security hardening basics.
- Secret handling and redaction rules.
- Cost optimization habits.
- Assistant evaluation basics.
- Production observability upgrade path.
- Optional advanced serving roadmap: vLLM, Triton, Ray, KServe, and GPU scheduling.
- Production-readiness review with local and CI release gates.

## Commercialization Track

The [commercialization roadmap](21-commercialization-roadmap.md) runs alongside the technical weeks: audience first, a design-partner wedge second, and paid tiers third. Completing a local technical week does not bypass its customer-discovery or phase-exit gates.

## Weeks 5-8 Alignment Rules

| Week | Open-source technical outcome | Customer value it prepares | Commercial boundary |
| --- | --- | --- | --- |
| 5 | Privacy-safe provider telemetry, aggregates, pricing inputs, and cost per successful evaluated analysis. | Makes provider reliability and unit economics visible. | Local or public measurement may proceed in Phase A. The Phase B metering milestone remains incomplete until design-partner usage is measurable. |
| 6 | Versioned public, synthetic, sanitized, and adversarial evaluation cases with machine-readable CI results. | Proves changes do not silently weaken grounding, usefulness, safety, privacy, or honesty. | Customer-private incidents enter only after Phase A discovery unlocks Phase B and the team approves the data boundary. |
| 7 | Optional local collection, stable signal contracts, one dashboard, and one alert-to-runbook exercise. | Proves the assistant can fit an operational workflow. | A real customer connector, authentication, and audit trail belong to Phase B; the local signal path does not authorize them automatically. |
| 8 | A reproducible deterministic/provider benchmark harness and a documented build-versus-buy decision. | Shows whether a private endpoint could improve a measured customer outcome. | Execute a private-endpoint or GPU experiment only for a named privacy, deployment, latency, availability, or economics requirement. |

The technical exit gates answer whether the foundation works. The commercialization exit gates answer whether customers need it, will use it repeatedly, and will pay for it. Both must pass before the project enters an internal pilot or paid tier.

## Week 5 - Provider Telemetry

- Day 1 - complete: expose a bounded per-call contract for provider/model identity, request latency, token usage, outcome, and deterministic fallback without storing sensitive content.
- Day 2: add aggregate counters and latency distributions with bounded labels.
- Day 3: define explicit pricing inputs and estimated cost metadata without hard-coding unstable provider prices.
- Day 4: join provider usage and cost with evaluation outcomes and calculate cost per successful evaluated analysis.
- Day 5: add a local comparison report across deterministic and configured provider paths.
- Day 6: exercise provider failure and fallback behavior end to end.
- Day 7: review the Week 5 technical exit gate and record the separate commercialization status.

See [Provider Telemetry Contract](22-provider-telemetry.md) for the Day 1 API contract, privacy boundary, and remaining-week sequence.

**Exit gate:** provider usage, reliability, and cost can be compared with evaluation outcomes without storing prompts, incident evidence, credentials, endpoints, or generated content.

## Week 6 - Evaluation Maturity

- Expand the public corpus with synthetic or approved sanitized incidents, adversarial inputs, prompt-injection cases, incorrect-confidence cases, and redaction edge cases.
- Keep customer-private incident sets behind the Phase B discovery and data-boundary gates.
- Version the corpus, assistant configuration, and acceptance thresholds together.
- Produce machine-readable evaluation results in CI.
- Keep privacy and safety as hard release gates.

**Exit gate:** a model, prompt, provider, or code change produces a repeatable regression report and cannot bypass required privacy or safety checks.

## Week 7 - Production Signal Path

- Standardize structured stdout logs and cross-service correlation fields.
- Add an optional OpenTelemetry Collector path after signal contracts are stable.
- Add a small dashboard and one actionable, owned alert.
- Exercise one incident from alert through evidence, assistant analysis, runbook action, and recovery review.

**Exit gate:** the project demonstrates a complete symptom-to-recovery workflow without changing the dependency-light quickstart.

## Week 8 - Provider Versus Private Endpoint Benchmark

- Build one harness that runs the same evaluation corpus against deterministic and managed-provider paths and can target an OpenAI-compatible private endpoint.
- Run a private-endpoint experiment only when a named customer or product requirement justifies it.
- Measure quality, latency, token usage, fallbacks, throughput, and cost per successful evaluated analysis.
- Test representative input sizes, concurrency, and burst behavior.
- Record a build-versus-buy decision before adding GPU infrastructure.

**Exit gate:** evidence supports continuing with a provider or, only when a named requirement exists, starting one bounded private-model experiment.

## Internal Pilot Phase

Begin only after the Week 5-8 measurement loop works and the commercialization roadmap has reached the design-partner phase with named owners.

- Authentication, service identity, and role-based access.
- Managed secrets, rotation, artifact pinning, and supply-chain scanning.
- Ingress, TLS, environment separation, and hardened deployment automation.
- Centralized telemetry, retention policies, audit records, quotas, and budgets.
- Initial SLOs, routed alerts, rollback tests, and recovery exercises.
- Private evaluation datasets and controlled evidence access.

**Exit gate:** a sanitized internal pilot can operate with explicit ownership, access controls, measurable reliability, and a tested rollback path.

## Advanced Serving Phase - Only If Earned

- Test one approved model behind an authenticated OpenAI-compatible endpoint.
- Add an optional single-GPU vLLM example only when the Week 8 benchmark or a named deployment requirement justifies it.
- Add GPU scheduling, quotas, utilization telemetry, queue metrics, and out-of-memory recovery tests for a real workload.
- Introduce Ray Serve, Triton, or KServe only when its specific orchestration problem appears.
- Consider enterprise VPC, dedicated, or on-premises packaging after customer demand is validated.

The default project remains deterministic, provider-compatible, laptop-friendly, and GPU-free throughout these phases.

## Longer-Term Product Backlog

- Hosted evaluation history and regression alerts.
- Team collaboration and private incident datasets.
- Audit-ready exports, policy controls, and usage governance.
- Privacy-aware product outcome telemetry.
- Provider and model quality/cost comparisons over time.
- Log, metrics, and trace backend examples using Prometheus, Grafana, compatible open-source components, or managed services.
- Multi-environment and cloud deployment examples.
- Horizontal Pod Autoscaling for measured non-GPU workloads.
