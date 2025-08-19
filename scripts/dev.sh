#!/usr/bin/env bash
set -euo pipefail

cd /workspace/backend
if command -v poetry >/dev/null 2>&1; then
  poetry install
else
  echo "Poetry not found. Please install Poetry or run backend manually."
fi

cd /workspace/frontend
if command -v npm >/dev/null 2>&1; then
  npm install
else
  echo "npm not found. Please install Node.js."
fi

echo "Setup complete. Start backend: cd /workspace/backend && poetry run uvicorn app.main:app --reload"
echo "Start frontend: cd /workspace/frontend && npm run dev"

