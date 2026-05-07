# Local Setup

## Requirements

- Docker
- Docker Compose
- Python 3.10 or newer for the traffic script
- Make, or the ability to run the commands from the `Makefile` manually

No GPU is required.

## Start

```bash
cp .env.example .env
make up
```

No `make` installed:

```bash
docker compose up --build -d
```

Check the services:

```bash
curl http://localhost:8000/health
curl http://localhost:8001/health
```

## Generate Signals

```bash
make generate-traffic
```

No `make` installed:

```bash
python scripts/generate-demo-traffic.py --base-url http://localhost:8000
```

This calls normal endpoints, error simulation, latency simulation, memory pressure, and not-found paths.

## Analyze

```bash
make analyze-logs
```

No `make` installed:

```bash
docker compose run --rm --no-deps ai-sre-assistant python cli/sre.py analyze --max-lines 120
```

The first run should work without an LLM key. That fallback is intentional.

## Stop

```bash
make down
```

No `make` installed:

```bash
docker compose down
```
