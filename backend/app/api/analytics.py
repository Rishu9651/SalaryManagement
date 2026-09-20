from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.analytics import (
    AnalyticsSummaryResponse,
    DimensionCompensationStats,
    SalaryDistributionResponse,
)
from app.services.analytics import (
    get_country_analytics,
    get_department_analytics,
    get_distribution,
    get_summary,
)


router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get(
    "/summary",
    response_model=AnalyticsSummaryResponse,
    summary="Get compensation summary",
    description="Summarize current compensation without combining currencies.",
)
def summary(session: Session = Depends(get_db)) -> AnalyticsSummaryResponse:
    return get_summary(session)


@router.get(
    "/countries",
    response_model=list[DimensionCompensationStats],
    summary="Get compensation by country",
)
def countries(session: Session = Depends(get_db)) -> list[DimensionCompensationStats]:
    return get_country_analytics(session)


@router.get(
    "/departments",
    response_model=list[DimensionCompensationStats],
    summary="Get compensation by department",
)
def departments(session: Session = Depends(get_db)) -> list[DimensionCompensationStats]:
    return get_department_analytics(session)


@router.get(
    "/salary-distribution",
    response_model=list[SalaryDistributionResponse],
    summary="Get current salary distribution",
)
def salary_distribution(
    session: Session = Depends(get_db),
) -> list[SalaryDistributionResponse]:
    return get_distribution(session)