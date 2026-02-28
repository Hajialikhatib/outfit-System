#!/bin/bash

# ==========================================
# Nguo System - Production Backend Start Script
# ==========================================

echo "🚀 Starting Nguo System Backend (Production)..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Virtual environment not found at ../.venv"
    echo "Please create and activate the virtual environment first:"
    echo "  python -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source ../.venv/bin/activate

# Set environment variables for production
export ENVIRONMENT=production
export DEBUG=False

# Collect static files (run this once during deployment)
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations (run this once during deployment)
echo "🗄️ Running migrations..."
python manage.py migrate

# Start Gunicorn
echo "🔄 Starting Gunicorn on port 8000..."
gunicorn -c gunicorn_config.py nguoSystem.wsgi:application
