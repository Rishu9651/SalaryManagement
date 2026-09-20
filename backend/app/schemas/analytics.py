from decimal import Decimal

from pydantic import BaseModel, Field


class CompensationStats(BaseModel):
    currency: str = Field(min_length=3, max_length=3)
    employee_count: int
    average_base_salary: Decimal | None
    total_base_salary: Decimal | None
    average_bonus: Decimal | None
    total_bonus: Decimal | None


class AnalyticsSummaryResponse(BaseModel):
    total_employees: int
    employees_with_salary: int
    compensation: list[CompensationStats]


class DimensionCompensationStats(CompensationStats):
    country: str | None = None
    department: str | None = None


class SalaryBand(BaseModel):
    label: str
    employee_count: int


class SalaryDistributionResponse(BaseModel):
    currency: str = Field(min_length=3, max_length=3)
    bands: list[SalaryBand]