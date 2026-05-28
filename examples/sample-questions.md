# Sample Questions

Use these against `POST /ask` or the CLI:

- Why is the demo service failing?
- What errors happened recently?
- What should I check next?
- Is this a latency issue, dependency issue, or application bug?
- Summarize the last incident.
- Which endpoint looks most suspicious?
- Are there signs of memory pressure?
- What evidence supports the likely root cause?
- What do the metrics say about the latest incident?

Example API request:

```bash
curl -s -X POST http://localhost:8001/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"Is this a latency issue, dependency issue, or application bug?","max_lines":120}'
```

Example metrics request:

```bash
curl -s -X POST http://localhost:8001/analyze/metrics \
  -H "Content-Type: application/json" \
  -d '{}'
```
