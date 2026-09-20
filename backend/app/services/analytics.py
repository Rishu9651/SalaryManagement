from __future__ import annotations

from decimal import Decimal

from sqlalchemy import and_, case
from sqlalchemy.orm import Session

from app.models.salary import SalaryRecord
from app.repositories.analytics import (
    get_compensation_by_currency,
    get_compensation_by_dimension,
    get_employees_with_salary_count,
    get_salary_distribution,
    get_total_employee_count,
)
from app.schemas.analytics import (
    AnalyticsSummaryResponse,
    CompensationStats,
    DimensionCompensationStats,
    SalaryBand,
    SalaryDistributionResponse,
)

COUNTRY_SALARY_BANDS: dict[str, tuple[tuple[str, Decimal | None, Decimal | None], ...]] = {
    "INR": (
        ("0-10L", Decimal("0"), Decimal("1000000")),
        ("10-20L", Decimal("1000000"), Decimal("2000000")),
        ("20-40L", Decimal("2000000"), Decimal("4000000")),
        ("40L+", Decimal("4000000"), None),
    ),
    "USD": (
        ("0-50K", Decimal("0"), Decimal("50000")),
        ("50-100K", Decimal("50000"), Decimal("100000")),
        ("100-150K", Decimal("100000"), Decimal("150000")),
        ("150K+", Decimal("150000"), None),
    ),
    "GBP": (
        ("0-40K", Decimal("0"), Decimal("40000")),
        ("40-80K", Decimal("40000"), Decimal("80000")),
        ("80-120K", Decimal("80000"), Decimal("120000")),
        ("120K+", Decimal("120000"), None),
    ),
    "EUR": (
        ("0-50K", Decimal("0"), Decimal("50000")),
        ("50-100K", Decimal("50000"), Decimal("100000")),
        ("100-150K", Decimal("100000"), Decimal("150000")),
        ("150K+", Decimal("150000"), None),
    ),
    "CAD": (
        ("0-60K", Decimal("0"), Decimal("60000")),
        ("60-100K", Decimal("60000"), Decimal("100000")),
        ("100-150K", Decimal("100000"), Decimal("150000")),
        ("150K+", Decimal("150000"), None),
    ),
    "AUD": (
        ("0-70K", Decimal("0"), Decimal("70000")),
        ("70-120K", Decimal("70000"), Decimal("120000")),
        ("120-170K", Decimal("120000"), Decimal("170000")),
        ("170K+", Decimal("170000"), None),
    ),
}


def _normalized_row(row) -> dict:
    values = dict(row)
    for field in (
        "average_base_salary",
        "total_base_salary",
        "average_bonus",
        "total_bonus",
    ):
        if values[field] is not None:
            values[field] = Decimal(str(values[field])).quantize(Decimal("0.01"))
    return values


def _compensation_stats(row) -> CompensationStats:
    return CompensationStats(**_normalized_row(row))


def get_summary(session: Session) -> AnalyticsSummaryResponse:
    return AnalyticsSummaryResponse(
        total_employees=get_total_employee_count(session),
        employees_with_salary=get_employees_with_salary_count(session),
        compensation=[
            _compensation_stats(row)
            for row in get_compensation_by_currency(session)
        ],
    )


def get_country_analytics(session: Session) -> list[DimensionCompensationStats]:
    return [
        DimensionCompensationStats(**_normalized_row(row))
        for row in get_compensation_by_dimension(session, "country")
    ]


def get_department_analytics(session: Session) -> list[DimensionCompensationStats]:
    return [
        DimensionCompensationStats(**_normalized_row(row))
        for row in get_compensation_by_dimension(session, "department")
    ]


def get_distribution(session: Session) -> list[SalaryDistributionResponse]:
    band_cases = []
    for currency, bands in COUNTRY_SALARY_BANDS.items():
        for label, lower, upper in bands:
            conditions = [SalaryRecord.currency == currency]
            if lower is not None:
                conditions.append(SalaryRecord.base_salary >= lower)
            if upper is not None:
                conditions.append(SalaryRecord.base_salary < upper)
            band_cases.append((and_(*conditions), label))

    band_expression = case(*band_cases, else_=None)
    counts = {
        (row["currency"], row["band"]): row["employee_count"]
        for row in get_salary_distribution(session, band_expression)
    }

    return [
        SalaryDistributionResponse(
            currency=currency,
            bands=[
                SalaryBand(
                    label=label,
                    employee_count=counts.get((currency, label), 0),
                )
                for label, _, _ in bands
            ],
        )
        for currency, bands in COUNTRY_SALARY_BANDS.items()
        if any((currency, label) in counts for label, _, _ in bands)
    ]