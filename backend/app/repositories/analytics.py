from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.salary import SalaryRecord


def _current_salary_join():
    return Employee.__table__.join(
        SalaryRecord.__table__,
        (SalaryRecord.employee_id == Employee.id)
        & SalaryRecord.effective_to.is_(None),
    )


def get_total_employee_count(session: Session) -> int:
    return session.scalar(select(func.count(Employee.id))) or 0


def get_employees_with_salary_count(session: Session) -> int:
    return (
        session.scalar(
            select(func.count(func.distinct(SalaryRecord.employee_id))).where(
                SalaryRecord.effective_to.is_(None)
            )
        )
        or 0
    )


def get_compensation_by_currency(session: Session):
    statement = (
        select(
            SalaryRecord.currency,
            func.count(SalaryRecord.employee_id).label("employee_count"),
            func.avg(SalaryRecord.base_salary).label("average_base_salary"),
            func.sum(SalaryRecord.base_salary).label("total_base_salary"),
            func.avg(SalaryRecord.bonus).label("average_bonus"),
            func.sum(SalaryRecord.bonus).label("total_bonus"),
        )
        .where(SalaryRecord.effective_to.is_(None))
        .group_by(SalaryRecord.currency)
        .order_by(SalaryRecord.currency)
    )
    return session.execute(statement).mappings().all()


def get_compensation_by_dimension(
    session: Session,
    dimension: str,
):
    dimension_column = {
        "country": Employee.country,
        "department": Employee.department,
    }[dimension]
    statement = (
        select(
            dimension_column.label(dimension),
            SalaryRecord.currency,
            func.count(SalaryRecord.employee_id).label("employee_count"),
            func.avg(SalaryRecord.base_salary).label("average_base_salary"),
            func.sum(SalaryRecord.base_salary).label("total_base_salary"),
            func.avg(SalaryRecord.bonus).label("average_bonus"),
            func.sum(SalaryRecord.bonus).label("total_bonus"),
        )
        .select_from(_current_salary_join())
        .group_by(dimension_column, SalaryRecord.currency)
        .order_by(dimension_column, SalaryRecord.currency)
    )
    return session.execute(statement).mappings().all()


def get_salary_distribution(
    session: Session,
    band_expression,
):
    statement = (
        select(
            SalaryRecord.currency,
            band_expression.label("band"),
            func.count(SalaryRecord.employee_id).label("employee_count"),
        )
        .where(SalaryRecord.effective_to.is_(None))
        .group_by(SalaryRecord.currency, band_expression)
        .order_by(SalaryRecord.currency, band_expression)
    )
    return session.execute(statement).mappings().all()