# ACME Salary Management System

## Project overview

ACME Salary Management System is a web application for managing employee and salary information for HR teams.

## Current tech stack

- Backend: Python, FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pytest
- Frontend: React, JavaScript, Vite, Axios

## Backend setup

From the repository root:

```powershell
.venv\Scripts\Activate.ps1
cd backend
python -m pip install -r requirements.txt
```

### PostgreSQL connection

Install native PostgreSQL for Windows and make sure the `postgresql-x64-18` service is running. The application uses the `salary_management` database.

Check the service and port:

```powershell
Get-Service postgresql-x64-18
Test-NetConnection localhost -Port 5432
```

Create the database with PostgreSQL's command-line tools:

```powershell
$env:PGPASSWORD="postgres"
& "C:\Program Files\PostgreSQL\18\bin\createdb.exe" `
	-h localhost `
	-p 5432 `
	-U postgres `
	salary_management
Remove-Item Env:PGPASSWORD
```

Copy the environment template once, then edit `backend/.env` if needed:

```powershell
Copy-Item backend\.env.example backend\.env -Force
```

`backend/.env` should contain the local connection URL:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/salary_management
```

The application and Alembic load this file automatically. It is ignored by Git and must not be committed.

Test the database directly:

```powershell
$env:PGPASSWORD="postgres"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" `
	-h localhost `
	-p 5432 `
	-U postgres `
	-d salary_management `
	-c "SELECT current_database();"
Remove-Item Env:PGPASSWORD
```

Apply and inspect migrations:

```powershell
python -m alembic upgrade head
python -m alembic current
```

Inspect tables from the terminal:

```powershell
$env:PGPASSWORD="postgres"
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" `
	-h localhost `
	-p 5432 `
	-U postgres `
	-d salary_management
```

Inside `psql`:

```sql
\dt
\d employees
\d salary_records
SELECT * FROM alembic_version;
\q
```

After leaving `psql`, clear the temporary password variable:

```powershell
Remove-Item Env:PGPASSWORD
```

Start the API:

```powershell
python -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Open interactive API documentation at `http://127.0.0.1:8000/docs`.

## Frontend setup

From the repository root:

```powershell
cd frontend
npm install
npm run dev
```

The Vite development server will print its local URL.

## Run tests

From the repository root, after installing backend dependencies:

```powershell
cd backend
python -m pytest
```

Run only the Employee and Salary API tests:

```powershell
python -m pytest tests/test_employee_api.py tests/test_salary_api.py
```