#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="/Users/aanyagarg/Desktop/PROJECT 1"
cd "$PROJECT_DIR"

stop_from_pid_file() {
  local name="$1"
  local pid_file=".pids/${name}.pid"
  if [ -f "$pid_file" ]; then
    local pid
    pid="$(cat "$pid_file" || true)"
    if [ -n "${pid:-}" ] && ps -p "$pid" >/dev/null 2>&1; then
      kill "$pid" >/dev/null 2>&1 || true
      echo "Stopped $name (pid $pid)"
    fi
    rm -f "$pid_file"
  fi
}

stop_from_pid_file "web"
stop_from_pid_file "rasa"

for port in 8010 8000 5005 5055; do
  pids="$(lsof -tiTCP:$port -sTCP:LISTEN || true)"
  if [ -n "$pids" ]; then
    kill $pids >/dev/null 2>&1 || true
    echo "Stopped process on port $port"
  fi
done
