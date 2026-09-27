@echo off
setlocal enabledelayedexpansion
title Aptimizer Civil AI - Desktop Launcher
color 0B

echo =====================================================================
echo           APTIMIZER CIVIL AI & ARCHITECTURAL DESIGN SUITE
echo                         Desktop Launcher
echo =====================================================================
echo.

set "ROOT_DIR=%~dp0"
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"

:: 1. Check MongoDB
echo [1/3] Verifying MongoDB database...
powershell -NoProfile -Command "if ((Get-Service -Name MongoDB -ErrorAction SilentlyContinue).Status -ne 'Running') { Start-Service -Name MongoDB -ErrorAction SilentlyContinue }"

:: 2. Check / Start Backend (Port 8000)
echo [2/3] Checking Backend API Server on port 8000...
netstat -ano | findstr ":8000 " | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [OK] Backend server is active on port 8000.
) else (
    echo [INFO] Starting Backend API server...
    start "Aptimizer Backend" /min cmd /c "cd /d "%ROOT_DIR%\backend" && python -m uvicorn server:app --host 127.0.0.1 --port 8000"
)

:: 3. Check / Start Frontend (Port 3000)
echo [3/3] Checking Frontend Web Interface on port 3000...
netstat -ano | findstr ":3000 " | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [OK] Frontend is active on port 3000.
) else (
    echo [INFO] Starting Frontend interface (compiling, please wait)...
    start "Aptimizer Frontend" /min cmd /c "cd /d "%ROOT_DIR%\frontend" && set BROWSER=none&& npm start"
)

:: Wait for Backend port 8000
echo.
echo Waiting for services to become ready...
set /a bcount=0
:WAIT_B
powershell -NoProfile -Command "try { $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8000/api/health' -UseBasicParsing -TimeoutSec 2; if ($r.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend server is healthy and responsive on port 8000.
    goto CHECK_F
)
set /a bcount+=1
if %bcount% geq 25 (
    echo [WARNING] Backend is taking longer than expected. Continuing...
    goto CHECK_F
)
timeout /t 1 /nobreak >nul
goto WAIT_B

:CHECK_F
:: Wait for Frontend port 3000
set /a fcount=0
:WAIT_F
netstat -ano | findstr ":3000 " | findstr "LISTENING" >nul
if %errorlevel% equ 0 (
    echo [OK] Frontend web interface is ready on port 3000.
    goto READY_LAUNCH
)
set /a fcount+=1
if %fcount% geq 45 (
    echo [WARNING] Frontend compilation is taking longer than expected. Launching anyway...
    goto READY_LAUNCH
)
timeout /t 1 /nobreak >nul
goto WAIT_F

:READY_LAUNCH
echo.
echo =====================================================================
echo Launching Aptimizer Application Window...
echo =====================================================================

:: Launch with direct browser executable path
if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app=http://localhost:3000 --window-size=1400,900
    goto OPENED
)
if exist "C:\Program Files\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files\Microsoft\Edge\Application\msedge.exe" --app=http://localhost:3000 --window-size=1400,900
    goto OPENED
)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://localhost:3000 --window-size=1400,900
    goto OPENED
)
if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --app=http://localhost:3000 --window-size=1400,900
    goto OPENED
)

:: Universal fallback
powershell -NoProfile -Command "Start-Process 'http://localhost:3000'"

:OPENED
echo.
echo [SUCCESS] Aptimizer application window opened!
timeout /t 2 /nobreak >nul 2>&1
exit
