# ACME Salary Management System

## Project overview

ACME Salary Management System is a web application for managing employee salary information. The repository currently contains the application foundation and database migration setup.

## Current tech stack

- Backend: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pytest
- Frontend: React, JavaScript, Vite, Axios

## Backend setup

From the repository root:

```powershell
.venv\Scripts\Activate.ps1
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, and the health endpoint is `GET /health`.

Set the PostgreSQL connection URL before using the database or Alembic:

```powershell
$env:DATABASE_URL="postgresql+psycopg://username:password@localhost:5432/acme_salary"
```

Run migrations from the `backend` directory:

```powershell
python -m alembic upgrade head
python -m alembic current
```

The initial migration is intentionally empty because employee and salary models are not part of the current stage.

## Frontend setup

From the repository root:

```powershell
cd frontend
npm install
npm run dev
```

The Vite development server will print its local URL.

## Run the health test

From the repository root, after installing backend dependencies:

```powershell
cd backend
python -m pytest
```