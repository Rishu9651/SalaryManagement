from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.salary import SalaryRecord
from app.repositories.employee import get_employee
from app.repositories.salary import (
    get_current_salary,
    get_overlapping_salaries,
)
from app.schemas.salary import SalaryCreate


class SalaryPeriodError(Exception):
    pass


def create_salary(
    session: Session,
    employee_id: int,
    data: SalaryCreate,
) -> SalaryRecord:
    employee = get_employee(session, employee_id)
    if employee is None:
        raise LookupError("Employee not found")

    overlapping = get_overlapping_salaries(
        session,
        employee_id,
        data.effective_from,
    )
    current = get_current_salary(session, employee_id)

    if overlapping:
        raise SalaryPeriodError("Salary effective date overlaps existing history")

    if current is not None:
        if current.effective_from >= data.effective_from:
            raise SalaryPeriodError(
                "New salary must start after the current salary period"
            )
        current.effective_to = data.effective_from - timedelta(days=1)

    salary = SalaryRecord(
        employee_id=employee_id,
        **data.model_dump(),
    )
    session.add(salary)
    session.commit()
    session.refresh(salary)
    return salary