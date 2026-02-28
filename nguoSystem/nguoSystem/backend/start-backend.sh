#!/bin/bash

echo "🧵 KUANZISHA DJANGO BACKEND..."
echo ""
echo "Port: 8000"
echo "URL: http://localhost:8000"
echo ""

cd /home/o-muhajir/nguoSystem/backend
source ../.venv/bin/activate
python manage.py runserver 0.0.0.0:8000
