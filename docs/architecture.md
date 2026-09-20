# Architecture

## 1. Overview

The application has three main parts:

- React + Vite frontend
- FastAPI backend
- PostgreSQL database

The frontend communicates with the backend through REST APIs. The backend handles validation, business rules, database access, and compensation analytics.

In production, the frontend runs on Vercel, the FastAPI backend runs on Render, and PostgreSQL is hosted on Neon.

## 2. Backend Structure

The FastAPI application starts from [backend/app/main.py](../backend/app/main.py).

The main application file registers the API routers, configures CORS from environment variables, and exposes the `/health` endpoint used for deployment checks.

The API code is separated by domain:

- [backend/app/api/employees.py](../backend/app/api/employees.py) handles employee creation, listing, updates, and deactivation.
- [backend/app/api/salary.py](../backend/app/api/salary.py) handles current salary, salary history, and salary changes.
- [backend/app/api/analytics.py](../backend/app/api/analytics.py) handles compensation summaries and salary breakdowns.

Business rules are kept outside the route handlers. The service and repository/data-access code handles validation, salary period logic, employee queries, and database operations.

Database configuration is handled through [backend/app/db/config.py](../backend/app/db/config.py) and [backend/app/db/session.py](../backend/app/db/session.py). The database URL is provided through environment configuration rather than being hardcoded.

Alembic is used for database migrations.

## 3. Frontend Structure

The frontend is a React application built with Vite and JavaScript.

The main application entry point is [frontend/src/App.jsx](../frontend/src/App.jsx). Pages and reusable UI components are kept under the `pages` and `components` directories.

API communication is centralized in [frontend/src/api/client.js](../frontend/src/api/client.js). The API base URL comes from the `VITE_API_BASE_URL` environment variable.

Domain-specific API modules under [frontend/src/api](../frontend/src/api) keep employee, salary, analytics, and other API calls separate from the page components.

The main user flows are:

- Dashboard and compensation analytics
- Employee list, search, filters, and pagination
- Employee details and salary history
- Adding and revising salary records

Employee data is loaded using server-side pagination and filtering instead of loading all employees into the browser.

## 4. Data Model

The main database tables are `employees` and `salary_records`.

The Employee model is defined in [backend/app/models/employee.py](../backend/app/models/employee.py).

The SalaryRecord model is defined in [backend/app/models/salary.py](../backend/app/models/salary.py).

An employee can have multiple salary records. A salary change creates a new salary record while the previous record is kept as history.

The current salary is represented by a salary record where `effective_to` is `NULL`. When a new salary becomes effective, the backend closes the previous salary period and creates the new current record.

This allows salary history to be retained instead of overwriting the previous salary.

## 5. Request Flow

A typical request follows this flow:

    React page
        ↓
    Axios API client
        ↓
    FastAPI router
        ↓
    Service / repository layer
        ↓
    SQLAlchemy
        ↓
    PostgreSQL
        ↓
    FastAPI response
        ↓
    React UI

For example, when the Employees page is opened, the frontend sends the requested page, page size, search term, and filters to the employee API.

The backend validates the request, applies the filters and pagination in the database query, and returns the requested records together with pagination information.

Analytics endpoints also perform aggregation in the database rather than loading all records into Python.

## 6. Production Setup

The deployed application uses:

    Vercel
       ↓
    React frontend
       ↓
    Render
       ↓
    FastAPI backend
       ↓
    Neon PostgreSQL

Environment variables are used for deployment-specific configuration.

The frontend uses:

    VITE_API_BASE_URL

The backend uses environment configuration for values such as:

    DATABASE_URL
    CORS_ORIGINS
    PORT

Database migrations and seed data are run explicitly rather than automatically during application startup.

## 7. Design Decisions

### Server-side pagination

Employee lists use database-level pagination because the application is designed around a dataset of approximately 10,000 employees.

### Database filtering

Search, country filtering, and department filtering are handled by the backend/database instead of filtering the complete employee list in the browser.

### Separate salary records

Salary records are stored separately from employee information so salary changes can be preserved as history.

### Database-side analytics

Summary, country, department, and salary distribution calculations use database aggregation rather than loading the complete dataset into application memory.

### Currency handling

Salary values are kept with their original currency. The application does not convert salaries between currencies, so values from different currencies are not combined into a single average or total.

### Database constraints

Important data integrity rules such as unique employee codes/emails and salary relationships are enforced at the database level in addition to application validation.

### Environment-based configuration

Database credentials, CORS origins, API URLs, and runtime configuration are provided through environment variables so local and production environments can use different settings without changing the application code.