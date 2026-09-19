from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.employee import get_employee
from app.repositories.salary import get_current_salary, get_salary_history
from app.schemas.salary import SalaryCreate, SalaryResponse
from app.services.salary import SalaryPeriodError, create_salary


router = APIRouter(prefix="/api/employees/{employee_id}", tags=["salary"])


@router.get("/salary", response_model=SalaryResponse, summary="Get current salary")
def get_current_employee_salary(
    employee_id: int,
    session: Session = Depends(get_db),
):
    if get_employee(session, employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    salary = get_current_salary(session, employee_id)
    if salary is None:
        raise HTTPException(status_code=404, detail="Salary has not been configured")
    return salary


@router.post(
    "/salary",
    response_model=SalaryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a salary record",
)
def create_employee_salary(
    employee_id: int,
    data: SalaryCreate,
    session: Session = Depends(get_db),
):
    try:
        return create_salary(session, employee_id, data)
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except SalaryPeriodError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error


@router.get(
    "/salary-history",
    response_model=list[SalaryResponse],
    summary="Get salary history",
)
def get_employee_salary_history(
    employee_id: int,
    session: Session = Depends(get_db),
):
    if get_employee(session, employee_id) is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return get_salary_history(session, employee_id)