from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.employee import Employee
from app.models.salary import SalaryRecord


def main() -> None:
    with SessionLocal() as session:
        employee_count = session.scalar(select(func.count()).select_from(Employee)) or 0
        salary_count = session.scalar(select(func.count()).select_from(SalaryRecord)) or 0
        seed_codes = [f"EMP{number:05d}" for number in range(1, 10_001)]
        seed_employee_ids = select(Employee.id).where(Employee.employee_code.in_(seed_codes))
        seed_employee_count = session.scalar(
            select(func.count()).select_from(Employee).where(
                Employee.employee_code.in_(seed_codes)
            )
        ) or 0
        distinct_codes = session.scalar(
            select(func.count(func.distinct(Employee.employee_code))).where(
                Employee.employee_code.in_(seed_codes)
            )
        ) or 0
        distinct_emails = session.scalar(
            select(func.count(func.distinct(Employee.email))).where(
                Employee.employee_code.in_(seed_codes)
            )
        ) or 0
        seed_salary_count = session.scalar(
            select(func.count()).select_from(SalaryRecord).where(
                SalaryRecord.employee_id.in_(seed_employee_ids)
            )
        ) or 0
        current_salary_count = session.scalar(
            select(func.count()).select_from(SalaryRecord).where(
                SalaryRecord.employee_id.in_(seed_employee_ids),
                SalaryRecord.effective_to.is_(None),
            )
        ) or 0

    print(f"employees={employee_count}")
    print(f"seed_employees={seed_employee_count}")
    print(f"distinct_employee_codes={distinct_codes}")
    print(f"distinct_emails={distinct_emails}")
    print(f"salary_records={salary_count}")
    print(f"seed_salary_records={seed_salary_count}")
    print(f"current_salary_records={current_salary_count}")

    if seed_employee_count != 10_000 or distinct_codes != seed_employee_count or distinct_emails != seed_employee_count:
        raise SystemExit("Seed employee verification failed")
    if seed_salary_count < 10_000 or current_salary_count != 10_000:
        raise SystemExit("Seed salary verification failed")


if __name__ == "__main__":
    main()