@echo off
REM ---------------------------------------------------------------------------
REM Aptimizer dev launcher — starts both servers, each in its own window.
REM
REM The backend runs with uvicorn --reload, so any .py change under backend\
REM (server.py, gis.py, engine.py, bim.py, siteplan\, ...) restarts it within
REM a second or two. No more editing a file and hitting 404s from a server
REM that predates the edit.
REM
REM Close a window to stop that server. Logs also land in tmp\backend.log and
REM tmp\frontend.log.
REM ---------------------------------------------------------------------------
cd /d "%~dp0backend"
start "Aptimizer backend (auto-reload)" cmd /k python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
cd /d "%~dp0frontend"
start "Aptimizer frontend" cmd /k npx craco start
