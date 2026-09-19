# ACME Salary Management System

## 1. Goal

ACME currently manages salary information for around 10,000 employees using Excel sheets. The goal of this project is to replace that process with a simple web application that allows HR managers to manage employee salary data and get useful insights from it.

The application should make common HR tasks such as finding an employee, checking their current salary, updating compensation, and understanding salary distribution easier and less dependent on manual spreadsheet work.

---

## 2. User

### Primary User

**HR Manager**

The HR manager should be able to:

- View the employee list
- Search and filter employees
- View employee details
- View current salary information
- Update an employee's salary
- View salary history
- Understand salary distribution across the organization

---

## 3. MVP Scope

### Employee Management

The application will support:

- Employee list
- Employee details
- Employee creation
- Employee update
- Employee deactivation
- Search by employee name or employee ID
- Filtering by country and department
- Pagination
- Sorting where required

The employee list will use server-side pagination so that all 10,000 employees are not loaded into the browser at once.

### Salary Management

HR managers will be able to:

- View an employee's current salary
- Update salary information
- Set an effective date for a salary change
- Add a reason for the salary change
- View previous salary records

Salary changes should not remove previous salary information. Each change will be stored as a separate salary record.

### Salary Analytics

The application will provide a dashboard with basic compensation insights, including:

- Total number of employees
- Average salary
- Salary distribution
- Employees by country
- Employees by department
- Average salary by country
- Average salary by department
- Employee count by salary range

### Multiple Countries

Employees can belong to different countries and salary records will store their currency.

For example:

- India - INR
- United States - USD
- United Kingdom - GBP
- Germany - EUR

The first version will display salaries in their original currency.

---

## 4. Data Seeding

The project will include a seed script that creates approximately 10,000 employees.

The generated data should contain realistic values for:

- Employee ID
- Name
- Email
- Country
- Department
- Job title
- Employment status
- Salary
- Currency

The seed script should be repeatable so that the database can easily be populated during development.

---

## 5. Technical Requirements

### Backend

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Pytest

The backend will expose REST APIs for employee management, salary management, and analytics.

### Frontend

- React
- JavaScript
- Axios
- A suitable component/UI library

The frontend will communicate with the FastAPI backend through REST APIs.

---

## 6. Main Screens

### Dashboard

The dashboard will provide a summary of the organization's compensation data.

It will show:

- Employee count
- Average salary
- Salary distribution
- Country breakdown
- Department breakdown

### Employees

The employee screen will provide:

- Search
- Filters
- Sorting
- Pagination
- Employee table
- Access to employee details

### Employee Details

The employee details screen will show:

- Basic employee information
- Current salary
- Currency
- Salary history
- Salary update option

### Analytics

The analytics screen will provide more detailed views of compensation by:

- Country
- Department
- Salary range

---

## 7. Non-Functional Requirements

### Performance

The application should be able to work with 10,000 employee records without loading the entire dataset into the browser.

Search, filtering, and pagination should be handled by the backend.

Frequently queried database fields should have appropriate indexes.

### Data Integrity

Salary updates should not overwrite historical salary information.

Invalid employee and salary data should be rejected by the backend.

API responses should use appropriate HTTP status codes.

### Maintainability

The backend should have a clear separation between:

- API routes
- Validation schemas
- Business logic
- Database models
- Data access

The frontend should keep API calls and reusable UI components separate from individual pages.

### Testing

The project should include automated tests for the important business logic.

Tests should cover areas such as:

- Employee operations
- Salary updates
- Salary history
- Search and filtering
- Pagination
- Analytics calculations
- Validation and error cases

---

## 8. Out of Scope

The following features are intentionally not part of the MVP.

### Payroll Processing

The application will not process employee payroll or make salary payments.

Payroll introduces additional requirements around deductions, taxes, benefits, payment processing, and compliance.

### Tax Calculation

Country-specific tax calculation is not included because tax rules can vary significantly between countries.

### Bank Integration

The application will not connect to banks or payment providers because payment processing is outside the main salary-management workflow.

### Employee Self-Service

Employees will not have their own portal in the first version. The application is focused on the HR Manager workflow.

### Benefits Management

Benefits such as insurance, healthcare, allowances, and other non-salary compensation are outside the initial scope.

### Real-Time Currency Conversion

The application will not use live foreign exchange rates in the MVP.

Salaries will remain associated with their original currency instead of converting all salaries into a single currency.

### Advanced Authorization

A complete role-based access control system is not required for the MVP. The initial product is designed around the HR Manager persona.

### AI-Based Salary Queries

The application will not depend on an AI/LLM system for its core analytics.

Basic salary questions can be answered using normal database queries, which keeps the results predictable and easier to test.

---

## 9. Important Design Decisions

### Salary History

Salary information will be stored separately from employee information.

This means that when an employee's salary changes, the previous salary record remains available.

This is important because HR may need to understand how compensation has changed over time.

### Server-Side Pagination

The backend will handle pagination instead of returning all employee records to the frontend.

This keeps API responses smaller and makes the application easier to scale beyond the initial 10,000 employees.

### Currency

Currency will be stored with each salary record.

The application will not compare raw salary numbers across different currencies because those values are not directly comparable.

### Simple Analytics

The first version will use deterministic database queries for salary analytics instead of introducing an AI system.

This keeps the results consistent and makes the calculations easier to test.

---

## 10. Success Criteria

The MVP will be considered complete when:

- An HR manager can access the application.
- The system can handle approximately 10,000 employees.
- Employees can be searched, filtered, sorted, and paginated.
- Employee details can be viewed and updated.
- Salary information can be updated.
- Previous salary records are preserved.
- Compensation analytics are available.
- Multiple countries and currencies are supported.
- Core backend functionality has automated tests.
- The application is deployed and accessible.
- A short video demonstrates the main workflows.

---

## 11. Possible Future Improvements

The following could be added in future versions:

- Authentication and SSO
- Role-based permissions
- Audit logs
- Bulk CSV import/export
- Salary approval workflow
- Employee self-service
- Payroll integration
- Benefits management
- Live currency conversion
- Compensation benchmarking
- Natural-language salary analytics
- Salary review notifications

These features are intentionally left out of the MVP so that the initial version stays focused on the core salary-management problem.