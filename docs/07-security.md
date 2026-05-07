# Security

The first version keeps secrets and risk simple.

## Local Secrets

Use `.env` for local configuration and keep it out of git. `.env.example` documents required variables without storing real keys.

## Assistant Safety

The assistant should avoid dangerous commands and avoid pretending it has evidence it does not have.

Good behavior:

- Say what is known.
- Say what is guessed.
- Cite evidence.
- Recommend low-risk checks first.

## Future Security Work

- Secret management for Kubernetes.
- Least-privilege service accounts.
- Network policies.
- Input and output filtering for assistant prompts.
- Audit logs for assistant actions.

