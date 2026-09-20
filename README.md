# ACME Salary Management System

## Project Overview

ACME Salary Management System is a web application for managing employee information, salary records, salary history, and compensation analytics for HR teams.

The application is designed around a workforce of approximately 10,000 employees across multiple countries.

## Live Application

Frontend:

https://salary-management-pied.vercel.app/

Backend API:

https://salary-management-api-fpev.onrender.com/

API Documentation:

https://salary-management-api-fpev.onrender.com/docs

## Main Features

### Employee Management

- View employees
- Search by employee name, employee code, or email
- Filter by country and department
- Server-side pagination
- Create employees
- Update employee information
- Deactivate employees

### Salary Management

- Add salary records
- View current salary
- View salary history
- Revise salary with an effective date
- Preserve previous salary records
- Support multiple currencies

### Compensation Analytics

The dashboard provides:

- Total employee count
- Employees with current salary
- Compensation by currency
- Country-level compensation
- Department-level compensation
- Salary distribution

Salary values are kept in their original currency. The application does not perform foreign exchange conversion.

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Pydantic
- Pytest

### Frontend

- React
- JavaScript
- Vite
- Axios

### Production

- Vercel - frontend
- Render - backend
- Neon - PostgreSQL

## Architecture

The main request flow is:

    React
       ↓
    Axios
       ↓
    FastAPI
       ↓
    SQLAlchemy
       ↓
    PostgreSQL

Production deployment:

    Vercel
       ↓
    React Frontend
       ↓
    Render
       ↓
    FastAPI Backend
       ↓
    Neon PostgreSQL

The backend uses environment variables for database configuration, CORS, and runtime settings. The frontend uses `VITE_API_BASE_URL` for the backend API URL.

More details are available in [docs/architecture.md](docs/architecture.md).

## Database Design

The main tables are:

    employees
        |
        | 1 : many
        v
    salary_records

Employee information is stored separately from salary records so salary changes can be preserved as history.

A current salary is represented by a salary record where `effective_to` is `NULL`.

Database migrations are managed using Alembic.

## Project Structure

    Salary Management/
    ├── backend/
    │   ├── app/
    │   ├── tests/
    │   ├── requirements.txt
    │   └── alembic.ini
    │
    ├── frontend/
    │   ├── src/
    │   ├── package.json
    │   └── ...
    │
    ├── docs/
    │   ├── requirements.md
    │   ├── architecture.md
    │   ├── deployment.md
    │   ├── performance-verification.md
    │   ├── testing.md
    │   ├── tradeoffs.md
    │   └── ai-prompts.md
    │
    └── README.md

## Local Setup

The following steps are for running the application locally.

### Prerequisites

Make sure the following are installed:

- Python 3.12+
- Node.js 18+
- npm
- PostgreSQL 18
- Git

### 1. Clone the Repository

```powershell
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd "Salary Management"

### 2. Create Python Environment

From the repository root:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Go to the backend directory:

```powershell
cd backend
```

Install backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Make sure the PostgreSQL service is running:

```powershell
Get-Service postgresql-x64-18
```

Check that PostgreSQL is listening on port `5432`:

```powershell
Test-NetConnection localhost -Port 5432
```

Create the database if it does not already exist:

```powershell
$env:PGPASSWORD="postgres"

& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" `
    -h localhost `
    -p 5432 `
    -U postgres `
    salary_management

Remove-Item Env:PGPASSWORD
```

### 4. Configure Backend Environment

From the `backend` directory, copy the environment template:

```powershell
Copy-Item .env.example .env -Force
```

Open `backend/.env` and configure the local PostgreSQL connection:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/salary_management
CORS_ORIGINS=http://localhost:5173
```

The `.env` file contains local configuration and should not be committed to Git.

### 5. Run Database Migrations

From the `backend` directory:

```powershell
python -m alembic upgrade head
```

Verify the current migration:

```powershell
python -m alembic current
```

### 6. Seed Development Data

Run the seed script:

```powershell
python -m app.seed
```

This creates approximately 10,000 employees and their salary records for local development and testing.

The seed process is explicit and does not run automatically when the application starts.

### 7. Start the Backend

From the `backend` directory:

```powershell
python -m uvicorn app.main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 8. Start the Frontend

Open a new terminal and go to the project root:

```powershell
cd "D:\Salary Management"
```

Go to the frontend directory:

```powershell
cd frontend
```

Install frontend dependencies:

```powershell
npm install
```

Create a `frontend/.env` file:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend development server:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

### 9. Verify the Local Application

Open the frontend:

```text
http://localhost:5173
```

Verify the following:

- Dashboard loads successfully
- Employee list is displayed
- Employee search works
- Country and department filters work
- Employee details can be viewed
- Salary information can be added or updated
- Salary history is displayed
- Compensation analytics are displayed

You can also verify the backend health endpoint:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 10. Run Tests

Run backend tests:

```powershell
cd backend
python -m pytest
```

Run frontend tests:

```powershell
cd frontend
npm test
```

Build the frontend for production:

```powershell
npm run build
```

### Local Application Flow

```text
Browser
   ↓
React + Vite
   ↓
Axios
   ↓
FastAPI
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

## Submission

### Repository

This repository contains the complete source code, tests, documentation, and deployment configuration for the Salary Management System.

### Project Artifacts

The following artifacts are included in the repository:

- [Requirements](docs/requirements.md) — Product requirements and project scope
- [Architecture](docs/architecture.md) — System architecture, components, request flow, and data model
- [AI Prompts and Instructions](docs/ai-prompts.md) — AI-assisted development approach and prompts
- [Technical Trade-offs](docs/tradeoffs.md) — Key technical decisions and alternatives considered
- [Testing](docs/testing.md) — Test coverage, test results, and testing approach
- [Performance Verification](docs/performance-verification.md) — Performance considerations and verification with the 10,000-employee dataset
- [Deployment](docs/deployment.md) — Production deployment and environment configuration

### Demo Video

The demo video covers:

- Application overview
- Employee management
- Employee search and filtering
- Salary management
- Salary history
- Compensation analytics
- Mock HR requests
- Request 05
- AI-assisted development
- Technical decisions and trade-offs
- Testing and performance considerations

**Demo Video:** [Watch the project demo](https://drive.google.com/file/d/18biRjYpWEnmMmp4IkZeDEeyjZgESWk0Q/view?usp=sharing)

### Live Application

**Frontend:** https://salary-management-pied.vercel.app/

**API Documentation:** https://salary-management-api-fpev.onrender.com/docs