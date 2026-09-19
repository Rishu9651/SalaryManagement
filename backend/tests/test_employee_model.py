import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.db.session import SessionLocal
from app.models.employee import Employee


def employee_data(code: str, email: str) -> dict[str, str]:
    return {
        "employee_code": code,
        "first_name": "John",
        "last_name": "Doe",
        "email": email,
        "country": "India",
        "department": "Engineering",
        "job_title": "Software Engineer",
    }


@pytest.fixture
def database_session():
    session = SessionLocal()
    created_codes: list[str] = []

    try:
        yield session, created_codes
    finally:
        session.rollback()

        for code in created_codes:
            employee = session.query(Employee).filter_by(
                employee_code=code
            ).first()

            if employee:
                session.delete(employee)

        session.commit()
        session.close()


def unique_value(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def test_employee_can_be_created(database_session) -> None:
    session, created_codes = database_session
    code = unique_value("EMP")
    email = f"{code.lower()}@example.com"

    employee = Employee(**employee_data(code, email))
    session.add(employee)
    created_codes.append(code)
    session.commit()
    session.refresh(employee)

    assert employee.id is not None
    assert employee.employee_code == code
    assert employee.email == email
    assert employee.status == "active"
    assert employee.created_at is not None
    assert employee.updated_at is not None


def test_employee_code_must_be_unique(database_session) -> None:
    session, created_codes = database_session
    code = unique_value("EMP")

    first_employee = Employee(
        **employee_data(code, f"{code.lower()}1@example.com")
    )
    session.add(first_employee)
    created_codes.append(code)
    session.commit()

    duplicate_employee = Employee(
        **employee_data(code, f"{code.lower()}2@example.com")
    )
    session.add(duplicate_employee)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_email_must_be_unique(database_session) -> None:
    session, created_codes = database_session
    code_one = unique_value("EMP")
    code_two = unique_value("EMP")
    email = f"{code_one.lower()}@example.com"

    first_employee = Employee(
        **employee_data(code_one, email)
    )
    session.add(first_employee)
    created_codes.append(code_one)
    session.commit()

    duplicate_employee = Employee(
        **employee_data(code_two, email)
    )
    session.add(duplicate_employee)
    created_codes.append(code_two)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_required_fields_are_enforced(database_session) -> None:
    session, created_codes = database_session
    code = unique_value("EMP")

    employee = Employee(
        employee_code=code,
        email=f"{code.lower()}@example.com",
    )
    session.add(employee)
    created_codes.append(code)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_status_defaults_to_active(database_session) -> None:
    session, created_codes = database_session
    code = unique_value("EMP")

    employee = Employee(
        **employee_data(code, f"{code.lower()}@example.com")
    )
    session.add(employee)
    created_codes.append(code)
    session.commit()
    session.refresh(employee)

    assert employee.status == "active"