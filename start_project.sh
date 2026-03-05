#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RASA_PORT="${RASA_PORT:-5005}"
WEB_PORT="${WEB_PORT:-8010}"

declare -a CANDIDATES=()
add_candidate() {
  local candidate="$1"
  [ -n "$candidate" ] || return 0
  for existing in "${CANDIDATES[@]:-}"; do
    [ "$existing" = "$candidate" ] && return 0
  done
  CANDIDATES+=("$candidate")
}

# Honor explicitly provided PYTHON_BIN first.
if [ -n "${PYTHON_BIN:-}" ]; then
  add_candidate "$PYTHON_BIN"
fi

# Active conda environment.
if [ -n "${CONDA_PREFIX:-}" ] && [ -x "${CONDA_PREFIX}/bin/python" ]; then
  add_candidate "${CONDA_PREFIX}/bin/python"
fi

# Common project-local virtual environment.
if [ -x "$PROJECT_DIR/.venv/bin/python" ]; then
  add_candidate "$PROJECT_DIR/.venv/bin/python"
fi

# Common named conda environment used by this project.
if command -v conda >/dev/null 2>&1; then
  CONDA_BASE="$(conda info --base 2>/dev/null || true)"
  if [ -n "${CONDA_BASE:-}" ] && [ -x "${CONDA_BASE}/envs/rasa_env/bin/python" ]; then
    add_candidate "${CONDA_BASE}/envs/rasa_env/bin/python"
  fi
fi

# Fallback system interpreters.
if command -v python3 >/dev/null 2>&1; then
  add_candidate "$(command -v python3)"
fi
if command -v python >/dev/null 2>&1; then
  add_candidate "$(command -v python)"
fi

PYTHON_BIN=""
for candidate in "${CANDIDATES[@]:-}"; do
  if [ -x "$candidate" ] && "$candidate" -c "import rasa" >/dev/null 2>&1; then
    PYTHON_BIN="$candidate"
    break
  fi
done

if [ -z "$PYTHON_BIN" ]; then
  for candidate in "${CANDIDATES[@]:-}"; do
    if [ -x "$candidate" ]; then
      PYTHON_BIN="$candidate"
      break
    fi
  done
fi

if [ -z "$PYTHON_BIN" ]; then
  echo "Python not found."
  echo "Install Python 3.10+ or set PYTHON_BIN=/path/to/python"
  exit 1
fi

cd "$PROJECT_DIR"
mkdir -p logs .pids models

echo "Project dir: $PROJECT_DIR"
echo "Using Python: $PYTHON_BIN"

if ! "$PYTHON_BIN" -c "import rasa" >/dev/null 2>&1; then
  echo "Rasa is not installed in this Python environment."
  echo "Run: \"$PYTHON_BIN\" -m pip install rasa"
  echo "Or activate the environment where Rasa is installed (example: conda activate rasa_env)."
  exit 1
fi

latest_model() {
  ls -t models/*.tar.gz 2>/dev/null | head -n 1 || true
}

if [ "${RETRAIN:-0}" = "1" ] || ! ls models/*.tar.gz >/dev/null 2>&1; then
  echo "Training model..."
  "$PYTHON_BIN" -m rasa train
fi

MODEL_FILE="${MODEL_FILE:-$(latest_model)}"
if [ -z "$MODEL_FILE" ]; then
  echo "No trained model found. Run: $PYTHON_BIN -m rasa train"
  exit 1
fi

port_is_open() {
  lsof -nP -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1
}

wait_for_port() {
  local port="$1"
  local timeout="$2"
  local i=0
  while [ "$i" -lt "$timeout" ]; do
    if port_is_open "$port"; then
      return 0
    fi
    sleep 1
    i=$((i + 1))
  done
  return 1
}

start_service() {
  local name="$1"
  local port="$2"
  local cmd="$3"
  local timeout="$4"

  if port_is_open "$port"; then
    echo "$name already running on :$port"
    return 0
  fi

  nohup bash -lc "$cmd" > "logs/${name}.log" 2>&1 &
  local pid=$!
  echo "$pid" > ".pids/${name}.pid"

  if wait_for_port "$port" "$timeout"; then
    echo "$name started on :$port"
  else
    echo "Failed to start $name. Check logs/${name}.log"
    exit 1
  fi
}

start_service "rasa" "$RASA_PORT" "cd '$PROJECT_DIR' && '$PYTHON_BIN' -m rasa run --model '$MODEL_FILE' --enable-api --cors '*' --port '$RASA_PORT'" 90
start_service "web" "$WEB_PORT" "cd '$PROJECT_DIR' && WEB_PORT='$WEB_PORT' RASA_ENDPOINT='http://127.0.0.1:$RASA_PORT/webhooks/rest/webhook' '$PYTHON_BIN' app.py" 20

echo
echo "Model:        $MODEL_FILE"
echo "Open website: http://127.0.0.1:${WEB_PORT}"
echo "Rasa status:  http://127.0.0.1:${RASA_PORT}/status"
