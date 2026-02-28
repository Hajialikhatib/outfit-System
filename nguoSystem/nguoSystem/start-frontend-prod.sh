#!/bin/bash

# ==========================================
# Nguo System - Production Frontend Start Script
# ==========================================

echo "🚀 Starting Nguo System Frontend (Production)..."
echo ""

# Navigate to frontend directory
cd "$(dirname "$0")/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "❌ node_modules not found. Installing dependencies..."
    npm install
fi

# Set production environment
export NODE_ENV=production

# Build the frontend
echo "📦 Building frontend for production..."
npm run build

# Preview the built application (or serve with a static file server)
echo "🌐 Starting production server on port 4173..."
npm run preview -- --host 0.0.0.0 --port 4173
