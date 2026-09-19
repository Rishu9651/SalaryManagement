from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.employee import Employee


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
    Base.metadata.create_all(bind=engine)


def teardown_function() -> None:
    Base.metadata.drop_all(bind=engine)


def employee_payload(
    code: str = "EMP001",
    email: str = "john@example.com",
    **overrides: str,
) -> dict[str, str]:
    payload = {
        "employee_code": code,
        "first_name": "John",
        "last_name": "Doe",
        "email": email,
        "country": "India",
        "department": "Engineering",
        "job_title": "Software Engineer",
    }
    payload.update(overrides)
    return payload


def create_employee(**overrides: str) -> dict:
    response = client.post("/api/employees", json=employee_payload(**overrides))
    assert response.status_code == 201
    return response.json()


def test_create_employee() -> None:
    employee = create_employee()

    assert employee["employee_code"] == "EMP001"
    assert employee["status"] == "active"
    assert "id" in employee
    assert "created_at" in employee


def test_invalid_employee_data_is_rejected() -> None:
    response = client.post(
        "/api/employees",
        json=employee_payload(email="not-an-email", first_name=""),
    )

    assert response.status_code == 422


def test_duplicate_employee_code_is_rejected() -> None:
    create_employee()

    response = client.post(
        "/api/employees",
        json=employee_payload(email="other@example.com"),
    )

    assert response.status_code == 409


def test_duplicate_email_is_rejected() -> None:
    create_employee()

    response = client.post(
        "/api/employees",
        json=employee_payload(code="EMP002"),
    )

    assert response.status_code == 409


def test_list_pagination_search_and_filters() -> None:
    create_employee(code="EMP001", email="john@example.com")
    create_employee(
        code="EMP002",
        email="jane@example.com",
        first_name="Jane",
        country="United States",
        department="Finance",
    )
    create_employee(
        code="EMP003",
        email="alex@example.com",
        first_name="Alex",
        country="India",
        department="Finance",
    )

    response = client.get(
        "/api/employees",
        params={"page": 1, "page_size": 2, "country": "India"},
    )
    body = response.json()

    assert response.status_code == 200
    assert body["total"] == 2
    assert len(body["items"]) == 2
    assert body["total_pages"] == 1

    response = client.get("/api/employees", params={"search": "jane"})
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["employee_code"] == "EMP002"

    response = client.get(
        "/api/employees",
        params={"search": "alex", "country": "India", "department": "Finance"},
    )
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["employee_code"] == "EMP003"


def test_pagination_returns_requested_page() -> None:
    for number in range(1, 4):
        create_employee(
            code=f"EMP00{number}",
            email=f"employee{number}@example.com",
        )

    response = client.get("/api/employees", params={"page": 2, "page_size": 2})
    body = response.json()

    assert body["total"] == 3
    assert body["page"] == 2
    assert [item["employee_code"] for item in body["items"]] == ["EMP003"]


def test_get_employee_and_missing_employee() -> None:
    employee = create_employee()

    response = client.get(f"/api/employees/{employee['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == employee["id"]

    response = client.get("/api/employees/9999")
    assert response.status_code == 404


def test_partial_update() -> None:
    employee = create_employee()

    response = client.patch(
        f"/api/employees/{employee['id']}",
        json={"department": "People Operations"},
    )

    assert response.status_code == 200
    assert response.json()["department"] == "People Operations"
    assert response.json()["first_name"] == "John"


def test_duplicate_values_are_rejected_during_update() -> None:
    first = create_employee()
    second = create_employee(code="EMP002", email="second@example.com")

    response = client.patch(
        f"/api/employees/{second['id']}",
        json={"email": first["email"]},
    )
    assert response.status_code == 409

    response = client.patch(
        f"/api/employees/{second['id']}",
        json={"employee_code": first["employee_code"]},
    )
    assert response.status_code == 409


def test_delete_deactivates_employee_without_removing_it() -> None:
    employee = create_employee()

    response = client.delete(f"/api/employees/{employee['id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "inactive"

    response = client.get(f"/api/employees/{employee['id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "inactive"

    response = client.delete(f"/api/employees/{employee['id']}")
    assert response.status_code == 200
    assert response.json()["status"] == "inactive"