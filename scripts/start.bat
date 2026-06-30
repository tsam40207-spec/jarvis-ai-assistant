@echo off
title JARVIS AI Executive Assistant
echo.
echo  ╔═══════════════════════════════════════╗
echo  ║     JARVIS AI EXECUTIVE ASSISTANT      ║
echo  ║         Starting all systems...        ║
echo  ╚═══════════════════════════════════════╝
echo.

:: Start Flask server in background
echo [1/3] Starting Flask backend...
start "Jarvis Backend" cmd /k "cd /d %~dp0..\backend && python server.py"
timeout /t 3 /nobreak >nul

:: Start HTTP server for dashboard
echo [2/3] Starting dashboard server...
start "Jarvis Dashboard" cmd /k "cd /d %~dp0..\frontend && python -m http.server 8080"
timeout /t 2 /nobreak >nul

:: Open dashboard in Chrome
echo [3/3] Opening Jarvis dashboard...
start chrome "http://localhost:8080"

echo.
echo  ✓ All systems online!
echo  ✓ Dashboard: http://localhost:8080
echo  ✓ Backend:   http://localhost:5000
echo.
echo  Say "Hi Jarvis" to get started!
echo.
pause
