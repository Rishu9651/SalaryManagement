from datetime import date

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.employee import Employee
from app.models.salary import SalaryRecord
from app.seed import COUNTRY_CURRENCIES, generate_seed_data, seed_database


def test_generated_seed_values_are_valid() -> None:
    rows = generate_seed_data(100, random_seed=7)

    codes = [row["employee"]["employee_code"] for row in rows]
    emails = [row["employee"]["email"] for row in rows]

    assert len(codes) == len(set(codes))
    assert len(emails) == len(set(emails))
    assert {row["employee"]["country"] for row in rows} <= set(COUNTRY_CURRENCIES)
    assert all(row["employee"]["status"] == "active" for row in rows)
    assert all(
        row["salary"]["currency"] == COUNTRY_CURRENCIES[row["employee"]["country"]]
        for row in rows
    )
    assert all(row["salary"]["base_salary"] > 0 for row in rows)
    assert all(row["salary"]["effective_to"] is None for row in rows)


def test_seed_creates_employee_with_current_salary_and_is_repeatable() -> None:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    test_session = sessionmaker(bind=engine, expire_on_commit=False)

    try:
        assert seed_database(3, session_factory=test_session) == 3
        assert seed_database(3, session_factory=test_session) == 0

        with test_session() as session:
            assert session.scalar(select(func.count()).select_from(Employee)) == 3
            assert session.scalar(select(func.count()).select_from(SalaryRecord)) == 3
            employee = session.scalar(
                select(Employee).where(Employee.employee_code == "EMP00001")
            )
            assert employee is not None
            assert len(employee.salary_records) == 1
            assert employee.salary_records[0].effective_from == date(2026, 1, 1)
            assert employee.salary_records[0].effective_to is None
    finally:
        Base.metadata.drop_all(engine)