#!/bin/bash
echo ""
echo "  ╔═══════════════════════════════════════╗"
echo "  ║     JARVIS AI EXECUTIVE ASSISTANT      ║"
echo "  ║         Starting all systems...        ║"
echo "  ╚═══════════════════════════════════════╝"
echo ""

# Start Flask backend
echo "[1/3] Starting Flask backend..."
cd "$(dirname "$0")/../backend"
python3 server.py &
BACKEND_PID=$!
sleep 3

# Start dashboard HTTP server
echo "[2/3] Starting dashboard server..."
cd "$(dirname "$0")/../frontend"
python3 -m http.server 8080 &
FRONTEND_PID=$!
sleep 2

# Open dashboard
echo "[3/3] Opening dashboard..."
if command -v xdg-open &> /dev/null; then
    xdg-open "http://localhost:8080"
elif command -v open &> /dev/null; then
    open "http://localhost:8080"
fi

echo ""
echo "  ✓ All systems online!"
echo "  ✓ Dashboard: http://localhost:8080"
echo "  ✓ Backend:   http://localhost:5000"
echo ""
echo "  Press Ctrl+C to stop all servers"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null" EXIT
wait
