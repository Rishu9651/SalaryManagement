from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SalaryCreate(BaseModel):
    base_salary: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    bonus: Decimal = Field(default=Decimal("0.00"), ge=0, max_digits=12, decimal_places=2)
    currency: str = Field(min_length=3, max_length=3, pattern=r"^[A-Za-z]{3}$")
    effective_from: date
    reason: str | None = Field(default=None, max_length=500)


class SalaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: int
    base_salary: Decimal
    bonus: Decimal
    currency: str
    effective_from: date
    effective_to: date | None
    reason: str | None
    created_at: datetime
    updated_at: datetime