# Technical Trade-offs

This project was kept intentionally simple for the current requirements. The main decisions were based on the expected 10,000 employee dataset, salary history requirements, and the need to keep the application easy to test and deploy.

## 1. PostgreSQL instead of SQLite

PostgreSQL was used even though SQLite was allowed by the assessment.

The application needs relational constraints, salary history, filtering, and grouped analytics. PostgreSQL also matches the production database used through Neon.

The trade-off is that local setup requires a PostgreSQL database instead of a single local database file.

## 2. Separate Employee and Salary Tables

Employee information and salary records are stored separately.

This makes salary history easier to maintain because a salary change creates a new record instead of overwriting the previous salary.

The trade-off is that current employee compensation requires a relationship between the two tables.

## 3. Server-Side Pagination

Employee listing uses server-side pagination instead of loading all 10,000 employees into the browser.

This keeps the amount of data returned per request small and allows search and filtering to happen in the database.

The trade-off is that the frontend needs to manage page, page size, filters, and total record information.

## 4. Database-Side Analytics

Analytics calculations are performed using SQL aggregation.

For example, compensation summaries are grouped by currency, country, or department in the database instead of loading all salary records into Python.

This reduces application-side processing and avoids unnecessary data transfer.

The trade-off is that some analytics logic is tied to SQL queries and needs to be updated when the reporting requirements change.

## 5. No Currency Conversion

Salary values are stored and displayed in their original currency.

The application does not convert INR, USD, GBP, EUR, CAD, or AUD into a common currency.

This avoids introducing an external exchange-rate dependency and prevents the application from presenting cross-currency comparisons as if they were directly comparable.

The trade-off is that users cannot see a single organization-wide salary total in one currency.

## 6. Soft Deactivation Instead of Hard Delete

Deleting an employee through the application changes the employee status to inactive instead of removing the database record.

This keeps the employee and salary history available for reporting and prevents accidental loss of historical data.

The trade-off is that inactive employees remain in the database and need to be filtered appropriately in future features.

## 7. Vercel + Render + Neon

The production deployment uses separate managed services:

- Vercel for the React frontend
- Render for the FastAPI backend
- Neon for PostgreSQL

This avoids managing a server or database infrastructure directly and keeps deployment relatively simple.

The trade-off is that the application depends on multiple external services instead of being deployed as one application.

## 8. No Additional Infrastructure

Redis, Kafka, background workers, caching, and other infrastructure were not added.

They were not required for the current salary management workflow, and adding them would increase deployment and maintenance complexity without solving a current requirement.

If the application later needs asynchronous processing, high-volume event handling, or more advanced caching, these components could be evaluated separately.