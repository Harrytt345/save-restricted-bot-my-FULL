#!/bin/bash

echo "=========================================="
echo "Starting Telegram Bot on Render"
echo "=========================================="

echo "Cleaning up old session files..."
rm -f *.session *.session-journal
echo "✓ Session files cleared"

echo "Creating necessary directories..."
mkdir -p downloads templates utils plugins
echo "✓ Directories created"

echo "Starting Flask web server in background..."
python3 app.py &
FLASK_PID=$!
echo "✓ Flask started (PID: $FLASK_PID)"

echo "Starting Telegram bot..."
python3 main.py
