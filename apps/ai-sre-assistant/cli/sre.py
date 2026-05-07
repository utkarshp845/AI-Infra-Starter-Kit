import argparse
import json
import sys
from pathlib import Path
from typing import Any


APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from app.analyzer import analyze_logs  # noqa: E402
from app.log_reader import get_log_path, read_recent_logs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze demo-service logs from the command line.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Summarize recent demo-service logs.")
    add_common_args(analyze_parser)

    ask_parser = subparsers.add_parser("ask", help="Ask an operational question about recent logs.")
    ask_parser.add_argument("question", help="Question to answer from recent log evidence.")
    add_common_args(ask_parser)

    args = parser.parse_args()
    log_path = Path(args.log_path) if args.log_path else get_log_path()
    question = getattr(args, "question", "What happened recently in demo-service logs?")

    logs = read_recent_logs(log_path=log_path, max_lines=args.max_lines)
    analysis = analyze_logs(logs, question=question)

    if args.json:
        print(json.dumps({"log_path": str(log_path), "logs_read": len(logs), "analysis": analysis}, indent=2))
    else:
        print_human_summary(log_path=log_path, logs_read=len(logs), analysis=analysis)

    return 0


def add_common_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--log-path", help="Path to the demo-service JSON log file.")
    parser.add_argument("--max-lines", type=int, default=120, help="Number of recent log lines to inspect.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON output.")


def print_human_summary(log_path: Path, logs_read: int, analysis: dict[str, Any]) -> None:
    print(f"Log path: {log_path}")
    print(f"Logs read: {logs_read}")
    print()
    print(f"Summary: {analysis['summary']}")

    print_section("Facts", analysis.get("facts", []))
    print_section("Likely causes / guesses", analysis.get("guesses", []))
    print_section("Evidence", [format_evidence(item) for item in analysis.get("evidence", [])])
    print_section("Safe next steps", analysis.get("next_steps", []))
    print_section("Possible fixes", analysis.get("possible_fixes", []))


def print_section(title: str, items: list[str]) -> None:
    if not items:
        return
    print()
    print(title + ":")
    for item in items:
        print(f"- {item}")


def format_evidence(item: dict[str, Any]) -> str:
    line = item.get("line", "?")
    event = item.get("event") or item.get("message") or "unknown"
    level = item.get("level", "unknown")
    path = item.get("path") or item.get("endpoint") or "unknown"
    status = item.get("status_code", "n/a")
    duration = item.get("duration_ms") or item.get("latency_ms") or "n/a"
    return f"line {line}: level={level} event={event} path={path} status={status} duration_ms={duration}"


if __name__ == "__main__":
    raise SystemExit(main())

