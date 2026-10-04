# Existing authentication verification

Read /app/memory/test_credentials.md. Do not seed or change credentials.
Use the current REACT_APP_BACKEND_URL from frontend/.env (do not reuse old previews).

1. Confirm MongoDB users.email unique index and login_attempts.identifier index exist. Inspect only the bcrypt hash prefix, never log the full hash.
2. POST /api/auth/login with the existing admin credentials and an Origin matching the frontend. Confirm 200, explicit Access-Control-Allow-Origin and credential support.
3. Use the returned cookies to GET /api/auth/me. Confirm the same account, no password fields, HttpOnly session cookies.
4. Log in through the real frontend. Confirm protected projects/workspace access and persistence after reload.
5. Confirm unapproved origins are not allowed. Allowed origins are FRONTEND_URL and optional comma-separated CORS_ORIGINS from backend/.env; never wildcard with credentials.

This pass changes only allowed-origin configuration. Password hashing, token logic, seeding and account data are unchanged.