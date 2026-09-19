from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.repositories.employee import get_employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeConflictError(Exception):
    pass


def create_employee(session: Session, data: EmployeeCreate) -> Employee:
    employee = Employee(**data.model_dump())
    session.add(employee)
    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise EmployeeConflictError from error
    session.refresh(employee)
    return employee


def update_employee(
    session: Session,
    employee_id: int,
    data: EmployeeUpdate,
) -> Employee | None:
    employee = get_employee(session, employee_id)
    if employee is None:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(employee, field, value)

    try:
        session.commit()
    except IntegrityError as error:
        session.rollback()
        raise EmployeeConflictError from error
    session.refresh(employee)
    return employee


def deactivate_employee(session: Session, employee_id: int) -> Employee | None:
    employee = get_employee(session, employee_id)
    if employee is None:
        return None
    employee.status = "inactive"
    session.commit()
    session.refresh(employee)
    return employee