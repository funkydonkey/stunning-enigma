#!/bin/bash

# Excel Formula Optimizer - Quick Start Script

echo "🚀 Starting Excel Formula Optimizer..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your ANTHROPIC_API_KEY"
    echo ""
    echo "Example:"
    echo "ANTHROPIC_API_KEY=your-api-key-here"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "✓ Activating virtual environment..."
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "Please run: uv sync"
    exit 1
fi

# Start the backend server
echo "✓ Starting FastAPI server on http://localhost:8000"
echo ""
echo "Access points:"
echo "  • Web Interface: http://localhost:8000"
echo "  • API Documentation: http://localhost:8000/docs"
echo ""
echo "The server serves both the frontend and API."
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --reload --port 8000
