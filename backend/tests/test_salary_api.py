from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

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


def override_get_db():
    with TestSession() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function() -> None:
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)


def teardown_function() -> None:
    Base.metadata.drop_all(bind=engine)


def employee_payload() -> dict[str, str]:
    return {
        "employee_code": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "country": "India",
        "department": "Engineering",
        "job_title": "Software Engineer",
    }


def create_employee() -> dict:
    response = client.post("/api/employees", json=employee_payload())
    assert response.status_code == 201
    return response.json()


def salary_payload(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "base_salary": "1500000.00",
        "bonus": "50000.00",
        "currency": "INR",
        "effective_from": "2025-01-01",
        "reason": "Initial salary",
    }
    payload.update(overrides)
    return payload


def create_salary(employee_id: int, **overrides: object) -> dict:
    response = client.post(
        f"/api/employees/{employee_id}/salary",
        json=salary_payload(**overrides),
    )
    assert response.status_code == 201
    return response.json()


def test_create_first_salary_and_get_current_salary() -> None:
    employee = create_employee()

    salary = create_salary(employee["id"])
    response = client.get(f"/api/employees/{employee['id']}/salary")

    assert response.status_code == 200
    assert salary["employee_id"] == employee["id"]
    assert response.json()["base_salary"] == "1500000.00"
    assert response.json()["effective_to"] is None


def test_salary_history_is_ordered_and_previous_period_is_closed() -> None:
    employee = create_employee()
    first = create_salary(employee["id"])
    second = create_salary(
        employee["id"],
        base_salary="1800000.00",
        effective_from="2026-09-19",
        reason="Annual review",
    )

    history = client.get(
        f"/api/employees/{employee['id']}/salary-history"
    ).json()
    current = client.get(f"/api/employees/{employee['id']}/salary").json()

    assert [record["id"] for record in history] == [second["id"], first["id"]]
    assert history[1]["effective_to"] == "2026-09-18"
    assert current["id"] == second["id"]
    assert current["effective_to"] is None


def test_salary_validation_rejects_negative_values_and_missing_currency() -> None:
    employee = create_employee()

    response = client.post(
        f"/api/employees/{employee['id']}/salary",
        json=salary_payload(base_salary="-1"),
    )
    assert response.status_code == 422

    response = client.post(
        f"/api/employees/{employee['id']}/salary",
        json=salary_payload(bonus="-1"),
    )
    assert response.status_code == 422

    payload = salary_payload()
    del payload["currency"]
    response = client.post(
        f"/api/employees/{employee['id']}/salary",
        json=payload,
    )
    assert response.status_code == 422


def test_invalid_and_overlapping_salary_dates_are_rejected() -> None:
    employee = create_employee()
    create_salary(employee["id"])

    response = client.post(
        f"/api/employees/{employee['id']}/salary",
        json=salary_payload(effective_from="2024-12-31"),
    )
    assert response.status_code == 422


def test_date_inside_closed_salary_period_is_rejected() -> None:
    employee = create_employee()
    create_salary(
        employee["id"],
        effective_from="2025-01-01",
    )
    create_salary(
        employee["id"],
        effective_from="2027-01-01",
    )

    response = client.post(
        f"/api/employees/{employee['id']}/salary",
        json=salary_payload(effective_from="2026-06-01"),
    )

    assert response.status_code == 422

    response = client.post(
        f"/api/employees/{employee['id']}/salary",
        json=salary_payload(effective_from="not-a-date"),
    )
    assert response.status_code == 422


def test_missing_employee_and_empty_history() -> None:
    response = client.get("/api/employees/9999/salary")
    assert response.status_code == 404

    response = client.get("/api/employees/9999/salary-history")
    assert response.status_code == 404

    employee = create_employee()
    response = client.get(f"/api/employees/{employee['id']}/salary-history")
    assert response.status_code == 200
    assert response.json() == []


def test_salary_is_associated_with_employee() -> None:
    employee = create_employee()
    salary = create_salary(employee["id"])

    with TestSession() as session:
        record = session.get(SalaryRecord, salary["id"])
        assert record is not None
        assert record.employee_id == employee["id"]
        assert record.employee.employee_code == "EMP001"
