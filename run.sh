#!/usr/bin/env sh
set -e
cd "$(dirname "$0")/backend"
if [ ! -x ".venv314/bin/python" ]; then
  python3.14 -m venv .venv314
  .venv314/bin/python -m pip install --upgrade pip
  .venv314/bin/python -m pip install -r requirements.txt
fi
exec .venv314/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
