import json
import os
from collections import deque
from pathlib import Path
from typing import Any

from app.redaction import redact_data, redact_text



DEFAULT_LOG_PATH = "logs/demo-service.log"


def get_log_path() -> Path:
    return Path(os.getenv("DEMO_SERVICE_LOG_PATH", DEFAULT_LOG_PATH))


def read_recent_lines(log_path: Path, max_lines: int = 100) -> list[dict[str, Any]]:
    if not log_path.exists():
        return []

    recent: deque[tuple[int, str]] = deque(maxlen=max_lines)
    with log_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:
                recent.append((line_number, line))

    return [{"line_number": line_number, "raw": raw} for line_number, raw in recent]


def parse_log_lines(lines: list[dict[str, Any]]) -> list[dict[str, Any]]:
    parsed = []
    for item in lines:
        raw = item["raw"]
        try:
            entry = json.loads(raw)
            if not isinstance(entry, dict):
                entry = {"message": str(entry)}
            entry["_line_number"] = item["line_number"]
            entry["_raw"] = redact_text(raw)
            parsed.append(redact_data(entry))
        except json.JSONDecodeError:
            parsed.append(
                {
                    "_line_number": item["line_number"],
                    "_raw": redact_text(raw),
                    "level": "WARNING",
                    "event": "malformed_log_line",
                    "message": "Log line could not be parsed as JSON.",
                    "malformed": True,
                }
            )

    return parsed


def read_recent_logs(log_path: Path | None = None, max_lines: int = 100) -> list[dict[str, Any]]:
    path = log_path or get_log_path()
    return parse_log_lines(read_recent_lines(path, max_lines=max_lines))

