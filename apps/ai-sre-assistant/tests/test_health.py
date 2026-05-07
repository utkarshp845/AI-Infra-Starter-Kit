from pathlib import Path

from fastapi.testclient import TestClient

from app.log_reader import read_recent_logs
from app.main import app


client = TestClient(app)


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
