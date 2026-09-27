# Aptimizer — PRD / Working Memory

## Original problem statement
User selected GitHub repo https://github.com/Anuj09k/Apt- as the root folder of this workspace. Plan: make changes on request; user saves/pushes via the platform "Save to Github" feature (agent cannot git-commit/push directly).

## Repo overview
- **Aptimizer**: civil engineering & real-estate planning platform (Indian IS/NBC codes, INR).
- Backend: FastAPI (`/app/backend/server.py`), MongoDB, uvicorn on port 8001 (supervisor).
- Frontend: React + craco (`/app/frontend`), port 3000, Tailwind.
- Git remote `origin` already points to Anuj09k/Apt- (main branch).

## Environment setup done (2026-09-27)
- Created `/app/backend/.env` (MONGO_URL local, DB_NAME=aptimizer, JWT_SECRET, ADMIN_*, FRONTEND_URL=preview URL) — gitignored, do not commit.
- Created `/app/frontend/.env` with REACT_APP_BACKEND_URL=preview URL.
- `yarn install --ignore-engines` in frontend (camera-controls requires node>=22; pod has node 20 — ignore-engines works).
- `/root/.venv/bin/pip install -r backend/requirements.txt` (supervisor uses /root/.venv).
- Backend /api/health = ok, DB healthy; admin seeded. Frontend loads (blueprint landing page).

## Implemented features
- (Baseline = repo as cloned; no feature changes yet.)

## Backlog / Next
- Awaiting user's requested changes.
- AI features (APT, AI reports, semantic code search) need GEMINI_API_KEY — currently disabled gracefully.
