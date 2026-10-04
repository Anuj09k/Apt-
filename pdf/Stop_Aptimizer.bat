@echo off
title Aptimizer - Shutdown Helper
color 0C
echo =====================================================================
echo                APTIMIZER CIVIL AI - STOP SERVICES
echo =====================================================================
echo.

echo [1/3] Terminating Aptimizer Desktop Tray Process...
taskkill /IM Aptimizer.exe /F >nul 2>&1
echo [OK] Desktop application closed.

echo.
echo [2/3] Terminating processes on port 8000 (Backend)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)
echo [OK] Backend stopped.

echo.
echo [3/3] Terminating processes on port 3000 (Frontend)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000 " ^| findstr "LISTENING"') do (
    taskkill /PID %%a /F >nul 2>&1
)
echo [OK] Frontend stopped.

echo.
echo =====================================================================
echo All Aptimizer application services have been stopped successfully.
echo =====================================================================
timeout /t 3 /nobreak >nul 2>&1
