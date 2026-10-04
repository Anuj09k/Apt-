@echo off
REM ---------------------------------------------------------------------------
REM Aptimizer dev launcher — starts both servers, each in its own window.
REM
REM The backend runs with uvicorn --reload, so any .py change under backend\
REM restarts it within a second or two.
REM
REM Close a window to stop that server.
REM ---------------------------------------------------------------------------
cd /d "%~dp0backend"
start "Aptimizer backend (auto-reload)" cmd /k python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
cd /d "%~dp0frontend"
start "Aptimizer frontend" cmd /k npm start
