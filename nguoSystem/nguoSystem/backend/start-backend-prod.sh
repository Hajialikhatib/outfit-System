#!/bin/bash
set -e

# ==========================================
# Nguo System - Production Backend Start Script
# Works locally (with .venv) AND on Render.com
# ==========================================

echo "Starting Nguo System Backend (Production)..."

# Navigate to the directory that contains this script
cd "$(dirname "$0")"

# ── Activate local venv only when running outside Render ──────────────────
if [ -z "$RENDER" ]; then
    VENV_PATH="../.venv"
    if [ -d "$VENV_PATH" ]; then
        echo "Activating local virtual environment..."
        source "$VENV_PATH/bin/activate"
    else
        echo "Warning: no local .venv found – using system Python"
    fi
fi

# ── Set production env vars (Render injects its own; these are local fallbacks)
export ENVIRONMENT=production
export DEBUG=${DEBUG:-False}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-nguoSystem.deployment}

# ── Determine port (Render sets $PORT automatically) ─────────────────────
PORT=${PORT:-8000}

echo "Starting Gunicorn on port $PORT..."
exec gunicorn nguoSystem.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers "${WEB_CONCURRENCY:-2}" \
    --threads 2 \
    --timeout 120 \
    --log-level warning
