from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.employee import get_employee, get_employee_page
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
)
from app.services.employee import (
    EmployeeConflictError,
    create_employee,
    deactivate_employee,
    update_employee,
)


router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post("", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED, summary="Create an employee")
def create_employee_endpoint(
    data: EmployeeCreate,
    session: Session = Depends(get_db),
):
    try:
        return create_employee(session, data)
    except EmployeeConflictError:
        raise HTTPException(
            status_code=409,
            detail="Employee code or email already exists",
        )


@router.get("", response_model=EmployeeListResponse, summary="List employees")
def list_employees(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    search: str | None = Query(default=None),
    country: str | None = Query(default=None, max_length=100),
    department: str | None = Query(default=None, max_length=100),
    session: Session = Depends(get_db),
):
    items, total = get_employee_page(
        session, page, page_size, search, country, department
    )
    return EmployeeListResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=ceil(total / page_size) if total else 0,
    )


@router.get("/{employee_id}",response_model=EmployeeResponse,summary="Get an employee",)
def get_employee_endpoint(
    employee_id: int,
    session: Session = Depends(get_db),
):
    employee = get_employee(session, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.patch("/{employee_id}",response_model=EmployeeResponse,summary="Update an employee",)
def update_employee_endpoint(
    employee_id: int,
    data: EmployeeUpdate,
    session: Session = Depends(get_db),
):
    try:
        employee = update_employee(session, employee_id, data)
    except EmployeeConflictError:
        raise HTTPException(
            status_code=409,
            detail="Employee code or email already exists",
        )
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.delete("/{employee_id}",response_model=EmployeeResponse,summary="Deactivate an employee",)
def delete_employee_endpoint(
    employee_id: int,
    session: Session = Depends(get_db),
):
    employee = deactivate_employee(session, employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee
