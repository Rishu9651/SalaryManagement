# ACME Salary Management System

## Project overview

ACME Salary Management System is a web application for managing employee salary information. This repository currently contains the initial project foundation only.

## Current tech stack

- Backend: Python, FastAPI, Pytest
- Frontend: React, JavaScript, Vite, Axios

## Backend setup

From the repository root:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, and the health endpoint is `GET /health`.

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
pytest
```