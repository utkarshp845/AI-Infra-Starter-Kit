# Security

Week 4 starts with security hardening basics.

The goal is not to turn the local learning lab into an enterprise platform in one day. The goal is to name the first risks clearly and build safer habits before production.

## Threat Model

The project flow is intentionally small:

```text
developer laptop
  -> demo-service
  -> logs / metrics
  -> ai-sre-assistant
  -> optional OpenAI-compatible LLM provider
```

Main risks:

- committing API keys or local secret files.
- leaking secrets into logs.
- sending sensitive logs to an external LLM provider.
- exposing local services publicly without auth.
- overtrusting assistant recommendations.
- using local Kubernetes shortcuts as if they were production architecture.
- running containers and clusters without least-privilege controls.

## Local Secrets

Use `.env` for local configuration and keep it out of git.

`.env.example` documents required variables without storing real keys.

Current local secret rules:

- `.env` should never be committed.
- `OPENAI_API_KEY` is optional.
- `LLM_PROVIDER=none` keeps the default rule-based path enabled.
- `infra/k8s/secret.example.yaml` is documentation only.
- `infra/k8s/secret.local.yaml` is ignored by git and should hold any real local Kubernetes Secret manifest.

If a key is ever committed, rotate it. Removing it from the latest commit is not enough.

## Kubernetes Secrets

Kubernetes Secrets are useful for teaching the first security primitive, but they are not the whole production answer.

For this repo:

- normal config belongs in `ConfigMap`.
- sensitive values belong in `Secret`.
- real secret manifests should stay local.
- screenshots should not show decoded secret values.

Production should consider external secret managers, encryption workflows, RBAC, rotation, and audit trails.

## Logs And Sensitive Data

The demo service intentionally emits logs for learning.

Do not put these values in logs:

- API keys.
- bearer tokens.
- passwords.
- private customer data.
- cloud credentials.
- raw authorization headers.

Before sharing logs publicly, redact values that identify private systems, accounts, users, or credentials.

## Assistant Safety

The AI SRE Assistant should be evidence-grounded and conservative.

Good behavior:

- say what is known.
- say what is guessed.
- cite log lines, metrics, or symptoms when possible.
- recommend low-risk checks first.
- avoid destructive commands.
- avoid pretending it has evidence it does not have.
- warn when logs or metrics may be incomplete.

Unsafe behavior:

- exposing secrets from logs.
- recommending destructive commands as a first step.
- claiming certainty without evidence.
- sending sensitive operational data to an external provider without review.
- treating LLM output as an automatic fix.

## LLM Provider Safety

The default assistant path does not need an LLM key.

When `LLM_PROVIDER=none`, the assistant uses deterministic rule-based analysis. This keeps the project useful without sending logs to an external provider.

Before enabling an external LLM provider:

- review what logs may be sent.
- remove secrets and sensitive data.
- understand the provider's data handling terms.
- avoid sending private production incidents from systems you do not own.

## Container And Dependency Basics

The first repo versions keep containers simple.

Production should add:

- dependency scanning.
- image scanning.
- non-root container users where practical.
- smaller runtime images.
- pinned dependency versions.
- regular rebuilds for base image updates.

These are later hardening steps. Day 1 of Week 4 is about naming the risks and creating guardrails.

## Service Exposure

Local services are not authenticated.

That is acceptable for a laptop-only learning lab. It is not acceptable as a production default.

Before exposing services outside a local machine:

- add authentication and authorization.
- use TLS.
- define public and private routes.
- restrict network access.
- review CORS and browser exposure.
- add audit logging for sensitive actions.

## Reporting Security Issues

See `../SECURITY.md` for vulnerability reporting guidance.

Do not open public issues that include real secrets, private logs, or credentials.

## Production Hardening Checklist

- Keep secrets out of git.
- Redact sensitive logs.
- Add auth before exposing services.
- Use external secret management for real deployments.
- Apply least-privilege RBAC.
- Review container users and permissions.
- Scan dependencies and images.
- Audit assistant access and outputs.
- Evaluate assistant recommendations before relying on them.
- Keep destructive actions human-approved.
