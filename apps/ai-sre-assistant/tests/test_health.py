from pathlib import Path

from fastapi.testclient import TestClient

from app.log_reader import read_recent_logs
from app.main import app
from app.metrics_analyzer import analyze_metrics
from app.metrics_reader import parse_prometheus_text


client = TestClient(app)


SAMPLE_METRICS = """
# HELP demo_service_http_requests_total Total HTTP requests handled by demo-service.
# TYPE demo_service_http_requests_total counter
demo_service_http_requests_total{method="GET",path="/health",status_code="200"} 4
demo_service_http_requests_total{method="GET",path="/simulate/error",status_code="500"} 2
demo_service_http_requests_total{method="GET",path="/simulate/latency",status_code="200"} 1
demo_service_http_request_duration_seconds_bucket{method="GET",path="/simulate/latency",le="1"} 0
demo_service_http_request_duration_seconds_count{method="GET",path="/simulate/latency"} 1
demo_service_simulated_errors_total{endpoint="/simulate/error",error_type="checkout_dependency_timeout"} 2
demo_service_simulated_latency_events_total{endpoint="/simulate/latency"} 1
demo_service_memory_pressure_events_total{endpoint="/simulate/memory-pressure"} 0
"""


def test_health_endpoint_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "ai-sre-assistant"}


def test_log_reader_parses_json_and_marks_malformed_lines(tmp_path: Path):
    log_file = tmp_path / "demo-service.log"
    log_file.write_text(
        '{"level":"ERROR","event":"simulated_error","message":"boom","status_code":500}\n'
        "this is not json\n",
        encoding="utf-8",
    )

    logs = read_recent_logs(log_path=log_file, max_lines=10)

    assert logs[0]["event"] == "simulated_error"
    assert logs[0]["_line_number"] == 1
    assert logs[1]["event"] == "malformed_log_line"
    assert logs[1]["malformed"] is True


def test_metrics_parser_and_analyzer_detect_incident_signals():
    samples = parse_prometheus_text(SAMPLE_METRICS)

    analysis = analyze_metrics(samples, source="test")

    assert analysis["signals"]["total_requests"] == 7
    assert analysis["signals"]["http_5xx"] == 2
    assert analysis["signals"]["simulated_errors"] == 2
    assert analysis["signals"]["simulated_latency_events"] == 1
    assert analysis["top_paths"][0] == {"path": "/health", "requests": 4}
    assert "exceeded 1 second" in analysis["latency_hints"][0]


def test_analyze_metrics_endpoint_accepts_metrics_text():
    response = client.post("/analyze/metrics", json={"metrics_text": SAMPLE_METRICS})

    assert response.status_code == 200
    body = response.json()
    assert body["analysis_mode"] == "rule-based"
    assert body["metrics_samples_read"] == 8
    assert body["metrics_analysis"]["signals"]["http_5xx"] == 2


def test_summarize_incident_includes_logs_and_metrics(tmp_path: Path, monkeypatch):
    log_file = tmp_path / "demo-service.log"
    log_file.write_text(
        '{"level":"ERROR","event":"simulated_error","message":"boom","endpoint":"/simulate/error","request_id":"req-1"}\n'
        '{"level":"INFO","event":"request_completed","message":"done","path":"/simulate/error","status_code":500,"request_id":"req-1"}\n',
        encoding="utf-8",
    )
    monkeypatch.setenv("DEMO_SERVICE_LOG_PATH", str(log_file))

    response = client.post(
        "/summarize-incident",
        json={"metrics_text": SAMPLE_METRICS, "max_lines": 20, "use_llm": False},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["log_analysis"]["summary"]
    assert body["metrics_analysis"]["signals"]["http_5xx"] == 2
    assert body["combined_analysis"]["summary"]
