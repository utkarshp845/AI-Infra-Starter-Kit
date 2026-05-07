# Architecture

The project uses two small services and one shared signal path.

```mermaid
flowchart LR
    user["User"] --> demo["demo-service<br/>FastAPI"]
    demo --> logs["shared JSON log file"]
    demo --> metrics["/metrics"]
    logs --> assistant["ai-sre-assistant<br/>FastAPI + CLI"]
    assistant --> rules["rule-based analyzer"]
    assistant --> llm["optional LLM provider"]
    rules --> answer["summary and safe next steps"]
    llm --> answer
    answer --> user
```

## Components

`demo-service` exists to produce realistic operational signals. It has healthy requests, intentional failures, latency spikes, memory pressure, and structured logs.

`ai-sre-assistant` exists to show how AI can help with operations when it is grounded in evidence. It reads logs, summarizes facts, makes limited guesses, and suggests safe debugging steps.

The shared file log is intentionally simple. It is not the production answer. It is the Day 1 bridge between a service and an assistant.

