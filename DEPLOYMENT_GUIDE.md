# Aptimizer Civil AI - Software Deployment & Packaging Guide

This guide covers how to deploy and run the **Aptimizer Civil AI & Architectural Design Suite** across different environments: as a local desktop software, in Docker containers, or on cloud servers.

---

## 🖥️ Option 1: Standalone Windows Desktop Software

You can run Aptimizer on Windows as a native desktop application with a single click.

### Quick Start:
1. **Double-Click:** `Launch_Aptimizer_Desktop.bat`
   - Automatically verifies the local MongoDB service.
   - Starts the FastAPI backend server on port 8000.
   - Starts the React frontend interface on port 3000.
   - Automatically opens in **Standalone Native App Mode** (using Edge or Chrome with `--app`), giving it a clean desktop window without browser bars, tabs, or URL inputs.
2. **Desktop Shortcut:**
   - Run `Create_Desktop_Shortcut.ps1` (or double-click the shortcut generated on your Desktop: `Aptimizer Civil AI.lnk`).
3. **Shutdown:**
   - Double-click `Stop_Aptimizer.bat` to gracefully terminate all backend and frontend services.

---

## 🐳 Option 2: Docker Container Deployment (Cloud VPS or Local)

The entire full stack (MongoDB, FastAPI Backend, React/Nginx Frontend) is containerized with Docker Compose.

### Requirements:
- Docker Engine & Docker Compose installed.

### Deploy in One Command:
```bash
# From the project root directory:
docker compose up -d --build
```

### What Happens:
- **`mongo`**: Launches official MongoDB 7.0 container with data persistence in a Docker volume.
- **`backend`**: Builds lightweight Python 3.11 container running FastAPI + Uvicorn on port 8000 with healthcheck.
- **`frontend`**: Multi-stage build producing an optimized Nginx container on port 80 that reverse-proxies `/api/` to the backend.

### Verify Deployment:
```bash
docker compose ps
docker compose logs -f
```
Open your browser to: `http://localhost`

### Enabling Automatic HTTPS (Public VPS / Domain):
Uncomment the `caddy` service in `docker-compose.yml`, specify your domain and email in `.env`:
```ini
DOMAIN=aptimizer.yourdomain.com
LETSENCRYPT_EMAIL=admin@yourdomain.com
```
Then run:
```bash
docker compose up -d
```
Caddy will automatically provision and renew a free Let's Encrypt SSL/TLS certificate.

---

## ☁️ Option 3: Cloud Web Service Deployment (PaaS / Serverless)

If deploying to platforms like Render, Railway, AWS, or DigitalOcean:

### 1. Database (MongoDB Atlas):
- Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/atlas).
- Copy the connection URI: `mongodb+srv://<user>:<password>@cluster0.mongodb.net/aptimizer`

### 2. Backend (Render / Railway / Cloud Run):
- Root directory: `./backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
- Environment Variables:
  - `MONGO_URL`: `<Your MongoDB Atlas connection URI>`
  - `DB_NAME`: `aptimizer`
  - `CORS_ORIGINS`: `*` (or your frontend domain)

### 3. Frontend (Vercel / Netlify / Cloudflare Pages):
- Root directory: `./frontend`
- Build command: `npm install --legacy-peer-deps && npm run build`
- Output directory: `build`
- Environment Variables:
  - `REACT_APP_BACKEND_URL`: `https://your-backend-api.onrender.com`

---

## 📦 Package Details
- **Architecture:** Microservices (React SPA + FastAPI REST/SSE + MongoDB Document Store)
- **Built Features:** 417 verified built features across 47 functional categories.
- **Standard References:** NBC 2016, IS 456:2000, IS 1893:2016, RERA norms.
