#!/usr/bin/env bash
set -euo pipefail

LOG_PATH="${DEMO_SERVICE_LOG_PATH:-logs/demo-service.log}"
LINES="${LINES:-80}"

if [ ! -f "$LOG_PATH" ]; then
  echo "No log file found at $LOG_PATH"
  echo "Start the stack and generate traffic first:"
  echo "  make up"
  echo "  make generate-traffic"
  exit 1
fi

tail -n "$LINES" -f "$LOG_PATH"

