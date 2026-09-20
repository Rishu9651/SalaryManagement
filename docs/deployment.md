# Deployment Guide

## Architecture

- Frontend: React + Vite deployed on Vercel
- Backend: FastAPI deployed on Render
- Database: PostgreSQL hosted on Neon

The frontend calls the backend through `VITE_API_BASE_URL`, and the backend reads `DATABASE_URL` from the environment.

## Backend deployment requirements

- Python runtime compatible with the FastAPI app and SQLAlchemy project.
- `DATABASE_URL` set from the environment.
- `PORT` set by the host platform.
- `CORS_ORIGINS` set to the exact allowed frontend origins.
- Run database migrations with Alembic before serving traffic.
- Keep `GET /health` available for health checks.
- Do not use `--reload` in production.
- Do not run the 10,000 employee seed automatically on app startup.

Production command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

This binds the app to the required network interface and deploy host port. The app also supports running as a module in environments that invoke `python -m app.main`.

## Frontend deployment requirements

- `VITE_API_BASE_URL` must be set to the production backend URL.
- Do not hardcode localhost URLs in React code or API clients.
- Use Vercel environment variables for production settings.
- Production build must succeed before deployment.

## Environment variables

### Backend

Example values:

```env
DATABASE_URL=postgresql+psycopg://username:password@host:5432/database
PORT=8000
CORS_ORIGINS=https://your-vercel-app.vercel.app,http://localhost:5173
ENVIRONMENT=production
```

- `DATABASE_URL`: PostgreSQL connection string for the deployed database.
- `PORT`: Port assigned by the host platform.
- `CORS_ORIGINS`: Comma-separated list of allowed frontend origins; do not use wildcard origins in production.
- `ENVIRONMENT`: Optional deployment identifier for local or production behavior.

### Frontend

```env
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com
```

## Alembic migration command

Run migrations explicitly before serving traffic:

```bash
cd backend
alembic upgrade head
```

If the runtime environment needs a migration command as part of deployment, use the same explicit Alembic command with the environment variables configured.

## Seed command

Seed data remains explicit and must not run automatically at application startup:

```bash
cd backend
python -m app.seed
```

This command inserts the 10,000 seeded employees and current salaries only when it is intentionally run.

## Health check

The backend exposes:

```http
GET /health
```

Expected response:

```json
{"status": "ok"}
```

## Local development configuration

### Backend

```bash
cd backend
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

Local frontend development should target:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Production configuration

- Backend served by Render with `DATABASE_URL` and `PORT` from environment variables.
- Frontend served by Vercel with `VITE_API_BASE_URL` pointing at the deployed Render backend.
- `CORS_ORIGINS` contains the deployed Vercel origin only, plus an explicit localhost origin for local development if needed.
- Database migrations are applied as a deployment step, not by `Base.metadata.create_all()`.
- The app does not seed data automatically during startup.
