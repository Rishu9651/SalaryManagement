from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models.employee import Employee


def get_employee(session: Session, employee_id: int) -> Employee | None:
    return session.get(Employee, employee_id)


def get_employee_page(
    session: Session,
    page: int,
    page_size: int,
    search: str | None,
    country: str | None,
    department: str | None,
) -> tuple[list[Employee], int]:
    query = select(Employee)
    count_query = select(func.count()).select_from(Employee)

    filters = []
    if search:
        search_term = f"%{search}%"
        filters.append(
            or_(
                Employee.employee_code.ilike(search_term),
                Employee.first_name.ilike(search_term),
                Employee.last_name.ilike(search_term),
                Employee.email.ilike(search_term),
            )
        )
    if country:
        filters.append(Employee.country == country)
    if department:
        filters.append(Employee.department == department)

    query = query.where(*filters).order_by(Employee.id)
    count_query = count_query.where(*filters)
    total = session.scalar(count_query) or 0
    items = session.scalars(
        query.offset((page - 1) * page_size).limit(page_size)
    ).all()
    return items, total