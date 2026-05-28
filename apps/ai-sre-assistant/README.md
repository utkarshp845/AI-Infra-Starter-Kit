# ai-sre-assistant

`ai-sre-assistant` reads recent `demo-service` logs and explains what happened in operational language.

It can use an OpenAI-compatible LLM provider for richer analysis. If no provider is configured, it uses a deterministic rule-based analyzer so the project works for everyone.

## API

- `GET /health`
- `POST /analyze/logs`
- `POST /analyze/metrics`
- `POST /ask`
- `POST /summarize-incident`

Example:

```bash
curl -s -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What errors happened recently?","max_lines":120}'
```

Analyze metrics:

```bash
curl -s -X POST http://localhost:8001/analyze/metrics \
  -H "Content-Type: application/json" \
  -d '{}'
```

Summarize an incident with logs and metrics:

```bash
curl -s -X POST http://localhost:8001/summarize-incident \
  -H "Content-Type: application/json" \
  -d '{"max_lines":120}'
```

## CLI

From the repository root after `make up` and `make generate-traffic`:

```bash
make analyze-logs
```

Or from this app directory:

```bash
python cli/sre.py analyze --log-path ../../logs/demo-service.log
python cli/sre.py ask "Is this a latency issue or an application bug?" --log-path ../../logs/demo-service.log
```

## LLM Configuration

The deterministic analyzer is the default. To use an LLM, update `.env`:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://api.openai.com/v1
MODEL_NAME=your_model
DEMO_SERVICE_METRICS_URL=http://localhost:8000/metrics
```

For local Ollama experiments, set `LLM_PROVIDER=ollama` and use an OpenAI-compatible Ollama base URL.
