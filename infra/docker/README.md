# Docker

Docker Compose is the Day 1 runtime for this project.

It starts:

- `demo-service` on port `8000`.
- `ai-sre-assistant` on port `8001`.

Both containers mount `./logs` to `/shared/logs`, which lets the assistant read the demo service log file.

## Commands

```bash
make up
make logs
make down
```

## Why Compose First

Compose keeps the first learning loop short:

- Build local images.
- Run multiple services.
- Share a local log volume.
- Avoid Kubernetes until the basic workflow is clear.

