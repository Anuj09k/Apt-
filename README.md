# Aptimizer

Civil engineering and real estate planning platform. Built for Indian codes (IS / NBC), money in INR.

## Quick start (development)

```
dev.bat
```

That single command opens two windows:

- **Aptimizer backend (auto-reload)** — FastAPI on `http://127.0.0.1:8000`, running
  under `uvicorn --reload`. Any `.py` change under `backend\` restarts the server
  within a second or two, so new or edited endpoints are live immediately — no more
  404s from a server that predates your edit.
- **Aptimizer frontend** — React (craco) on `http://localhost:3000`, with webpack
  hot reload.

Close a window to stop that server. Logs also land in `tmp\backend.log` and
`tmp\frontend.log`.

### Manual start (equivalent)

```bash
cd backend  && python -m uvicorn server:app --host 127.0.0.1 --port 8000 --reload
cd frontend && npx craco start
```

### Tests / production build

```bash
cd backend  && python -m pytest -q
cd frontend && npm run build        # goes through craco; do not invoke react-scripts directly
```

Requirements: Python 3.11+ with `backend/requirements.txt` installed (includes
`watchfiles`, which powers `--reload`), Node 18+ with `frontend/node_modules`,
and a local MongoDB on port 27017.
