import os
import re
from dataclasses import dataclass

import httpx


DEFAULT_METRICS_URL = "http://demo-service:8000/metrics"
METRIC_RE = re.compile(
    r"^(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)(?:\{(?P<labels>[^}]*)\})?\s+"
    r"(?P<value>[-+]?(?:[0-9]*\.)?[0-9]+(?:[eE][-+]?[0-9]+)?)$"
)


@dataclass(frozen=True)
class MetricSample:
    name: str
    labels: dict[str, str]
    value: float


def get_metrics_url() -> str:
    return os.getenv("DEMO_SERVICE_METRICS_URL", DEFAULT_METRICS_URL)


def fetch_metrics_text(metrics_url: str | None = None) -> tuple[str | None, str | None]:
    url = metrics_url or get_metrics_url()
    try:
        with httpx.Client(timeout=5) as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text, None
    except Exception as exc:
        return None, f"Could not fetch metrics from {url}: {exc}"


def parse_prometheus_text(metrics_text: str) -> list[MetricSample]:
    samples = []
    for raw_line in metrics_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        match = METRIC_RE.match(line)
        if not match:
            continue

        samples.append(
            MetricSample(
                name=match.group("name"),
                labels=_parse_labels(match.group("labels") or ""),
                value=float(match.group("value")),
            )
        )

    return samples


def _parse_labels(raw_labels: str) -> dict[str, str]:
    labels = {}
    for key, value in re.findall(r'([a-zA-Z_][a-zA-Z0-9_]*)="((?:\\.|[^"\\])*)"', raw_labels):
        labels[key] = _unescape_label(value)
    return labels


def _unescape_label(value: str) -> str:
    return value.replace(r"\n", "\n").replace(r"\"", '"').replace(r"\\", "\\")
