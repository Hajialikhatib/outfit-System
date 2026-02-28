#!/bin/bash

# Nguo System - Development Server Startup Script
# Skriti hii inaanzisha Django backend na React frontend pamoja

echo "🧵 Kuanzisha Nguo System..."
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment haipatikani!"
    echo "Tengeneza virtual environment kwanza: python3 -m venv .venv"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check if dependencies are installed
echo "✓ Kuangalia dependencies..."
python -c "import django" 2>/dev/null || {
    echo "❌ Django haijasanikishwa!"
    echo "Sanikisha dependencies: pip install -r requirements.txt"
    exit 1
}

# Check if frontend dependencies are installed
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend dependencies hazijasanikishwa!"
    echo "Sanikisha: cd frontend && npm install"
    exit 1
fi

# Start Django backend in background
echo "🚀 Kuanzisha Django backend (Port 8000)..."
cd backend
python manage.py runserver 0.0.0.0:8000 > /dev/null 2>&1 &
DJANGO_PID=$!
cd ..

# Wait for Django to start
sleep 2

# Start React frontend in background
echo "⚛️  Kuanzisha React frontend (Port 5173)..."
cd frontend
npm run dev > /dev/null 2>&1 &
VITE_PID=$!

cd ..

echo ""
echo "✅ Nguo System imeanza!"
echo ""
echo "📍 Backend:  http://localhost:8000"
echo "📍 Frontend: http://localhost:5173"
echo "📍 Admin:    http://localhost:8000/admin"
echo ""
echo "⏹️  Ili kuacha, bonyeza CTRL+C"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Kuacha Nguo System..."
    kill $DJANGO_PID 2>/dev/null
    kill $VITE_PID 2>/dev/null
    exit 0
}

# Trap CTRL+C
trap cleanup INT

# Wait for processes
wait
