from datetime import date
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.employee import Employee
from app.models.salary import SalaryRecord


engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
client = TestClient(app)


def override_get_db():
    with TestSession() as session:
        yield session


def add_employee(
    session,
    code: str,
    country: str,
    department: str,
) -> Employee:
    employee = Employee(
        employee_code=code,
        first_name="Test",
        last_name=code,
        email=f"{code.lower()}@example.com",
        country=country,
        department=department,
        job_title="Analyst",
    )
    session.add(employee)
    session.flush()
    return employee


def add_salary(
    session,
    employee: Employee,
    amount: str,
    currency: str,
    bonus: str = "0",
    effective_to: date | None = None,
) -> None:
    session.add(
        SalaryRecord(
            employee_id=employee.id,
            base_salary=Decimal(amount),
            bonus=Decimal(bonus),
            currency=currency,
            effective_from=date(2025, 1, 1),
            effective_to=effective_to,
            reason="Test data",
        )
    )


@pytest.fixture(autouse=True)
def analytics_database():
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    with TestSession() as session:
        india_engineer_one = add_employee(session, "EMP001", "India", "Engineering")
        india_engineer_two = add_employee(session, "EMP002", "India", "Engineering")
        usd_engineer = add_employee(session, "EMP003", "United States", "Engineering")
        no_salary = add_employee(session, "EMP004", "India", "Finance")
        current_with_history = add_employee(session, "EMP005", "India", "Engineering")
        historical_only = add_employee(session, "EMP006", "Germany", "Finance")

        add_salary(session, india_engineer_one, "1000000", "INR", "100000")
        add_salary(session, india_engineer_two, "3000000", "INR", "300000")
        add_salary(session, usd_engineer, "100000", "USD", "10000")
        add_salary(
            session,
            current_with_history,
            "500000",
            "INR",
            "50000",
            effective_to=date(2025, 12, 31),
        )
        add_salary(session, current_with_history, "2000000", "INR", "200000")
        add_salary(
            session,
            historical_only,
            "60000",
            "EUR",
            "6000",
            effective_to=date(2025, 12, 31),
        )
        session.commit()

    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.pop(get_db, None)


def test_summary_aggregates_current_salaries_by_currency() -> None:
    response = client.get("/api/analytics/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["total_employees"] == 6
    assert body["employees_with_salary"] == 4

    compensation = {item["currency"]: item for item in body["compensation"]}
    assert set(compensation) == {"INR", "USD"}
    assert compensation["INR"] == {
        "currency": "INR",
        "employee_count": 3,
        "average_base_salary": "2000000.00",
        "total_base_salary": "6000000.00",
        "average_bonus": "200000.00",
        "total_bonus": "600000.00",
    }
    assert compensation["USD"]["employee_count"] == 1
    assert compensation["USD"]["total_base_salary"] == "100000.00"


def test_country_and_department_analytics_group_by_currency() -> None:
    countries = client.get("/api/analytics/countries").json()
    country_rows = {(row["country"], row["currency"]): row for row in countries}
    assert country_rows[("India", "INR")]["employee_count"] == 3
    assert country_rows[("India", "INR")]["total_base_salary"] == "6000000.00"
    assert country_rows[("United States", "USD")]["employee_count"] == 1
    assert all(row["country"] != "Germany" for row in countries)

    departments = client.get("/api/analytics/departments").json()
    department_rows = {
        (row["department"], row["currency"]): row for row in departments
    }
    assert department_rows[("Engineering", "INR")]["employee_count"] == 3
    assert department_rows[("Engineering", "USD")]["employee_count"] == 1
    assert all(row["department"] != "Finance" for row in departments)


def test_salary_distribution_uses_currency_bands_and_current_records() -> None:
    response = client.get("/api/analytics/salary-distribution")

    assert response.status_code == 200
    distributions = {item["currency"]: item["bands"] for item in response.json()}
    assert set(distributions) == {"INR", "USD"}
    india_bands = {band["label"]: band["employee_count"] for band in distributions["INR"]}
    usd_bands = {band["label"]: band["employee_count"] for band in distributions["USD"]}
    assert india_bands["0-10L"] == 0
    assert india_bands["10-20L"] == 1
    assert india_bands["20-40L"] == 2
    assert usd_bands["0-50K"] == 0
    assert usd_bands["50-100K"] == 0
    assert usd_bands["100-150K"] == 1


def test_analytics_return_empty_salary_results_without_404() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestSession() as session:
        add_employee(session, "EMP100", "India", "Engineering")
        session.commit()

    summary = client.get("/api/analytics/summary")
    assert summary.status_code == 200
    assert summary.json() == {
        "total_employees": 1,
        "employees_with_salary": 0,
        "compensation": [],
    }
    assert client.get("/api/analytics/countries").json() == []
    assert client.get("/api/analytics/departments").json() == []
    assert client.get("/api/analytics/salary-distribution").json() == []