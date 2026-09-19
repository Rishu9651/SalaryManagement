from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.salary import SalaryRecord


def get_current_salary(session: Session, employee_id: int) -> SalaryRecord | None:
    return session.scalar(
        select(SalaryRecord).where(
            SalaryRecord.employee_id == employee_id,
            SalaryRecord.effective_to.is_(None),
        )
    )


def get_salary_history(session: Session, employee_id: int) -> list[SalaryRecord]:
    return list(
        session.scalars(
            select(SalaryRecord)
            .where(SalaryRecord.employee_id == employee_id)
            .order_by(SalaryRecord.effective_from.desc())
        ).all()
    )


def get_overlapping_salaries(
    session: Session,
    employee_id: int,
    effective_from: date,
) -> list[SalaryRecord]:
    return list(
        session.scalars(
            select(SalaryRecord)
            .where(
                SalaryRecord.employee_id == employee_id,
                SalaryRecord.effective_from <= effective_from,
                SalaryRecord.effective_to.is_not(None),
                SalaryRecord.effective_to >= effective_from,
            )
            .order_by(SalaryRecord.effective_from)
        ).all()
    )