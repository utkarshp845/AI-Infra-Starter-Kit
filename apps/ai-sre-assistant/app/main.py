from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.analyzer import analyze_logs
from app.llm import analyze_with_llm
from app.log_reader import get_log_path, read_recent_logs


app = FastAPI(
    title="ai-sre-assistant",
    description="An evidence-grounded operational assistant for the demo-service.",
    version="0.1.0",
)


class AnalyzeLogsRequest(BaseModel):
    max_lines: int = Field(default=100, ge=1, le=1000)
    use_llm: bool = True


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    max_lines: int = Field(default=100, ge=1, le=1000)
    use_llm: bool = True


class SummarizeIncidentRequest(BaseModel):
    max_lines: int = Field(default=200, ge=1, le=1000)
    use_llm: bool = True


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy", "service": "ai-sre-assistant"}


@app.post("/analyze/logs")
def analyze_recent_logs(request: AnalyzeLogsRequest) -> dict[str, Any]:
    return _analyze(question="What happened recently in demo-service logs?", max_lines=request.max_lines, use_llm=request.use_llm)


@app.post("/ask")
def ask(request: AskRequest) -> dict[str, Any]:
    return _analyze(question=request.question, max_lines=request.max_lines, use_llm=request.use_llm)


@app.post("/summarize-incident")
def summarize_incident(request: SummarizeIncidentRequest) -> dict[str, Any]:
    return _analyze(question="Summarize the last incident in the demo-service logs.", max_lines=request.max_lines, use_llm=request.use_llm)


def _analyze(question: str, max_lines: int, use_llm: bool) -> dict[str, Any]:
    log_path = get_log_path()
    logs = read_recent_logs(log_path=log_path, max_lines=max_lines)
    rule_based = analyze_logs(logs, question=question)

    response: dict[str, Any] = {
        "question": question,
        "analysis_mode": "rule-based",
        "log_path": str(log_path),
        "logs_read": len(logs),
        "rule_based_analysis": rule_based,
    }

    if use_llm:
        llm_analysis, llm_notice = analyze_with_llm(question=question, logs=logs, rule_based_analysis=rule_based)
        if llm_analysis:
            response["analysis_mode"] = "llm"
            response["llm_analysis"] = llm_analysis
        if llm_notice:
            response["llm_notice"] = llm_notice

    return response
