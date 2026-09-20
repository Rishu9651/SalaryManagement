from __future__ import annotations

import random
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any, Callable

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.salary import SalaryRecord

SEED_SIZE = 10_000
DEFAULT_SEED = 20260920
DEFAULT_EFFECTIVE_FROM = date(2026, 1, 1)
DEFAULT_CREATED_AT = datetime(2026, 1, 1, tzinfo=timezone.utc)

COUNTRY_CURRENCIES = {
    "India": "INR",
    "United States": "USD",
    "United Kingdom": "GBP",
    "Germany": "EUR",
    "Canada": "CAD",
    "Australia": "AUD",
}

COUNTRIES = tuple(COUNTRY_CURRENCIES)
DEPARTMENTS = (
    "Engineering",
    "Product",
    "Finance",
    "Human Resources",
    "Sales",
    "Marketing",
    "Operations",
    "Legal",
    "Customer Support",
)

FIRST_NAMES = (
    "Aarav", "Aisha", "Alexander", "Amelia", "Arjun", "Chloe", "Daniel",
    "Ethan", "Fatima", "Grace", "Hannah", "Henry", "Isabella", "James",
    "Karan", "Liam", "Lucas", "Maya", "Meera", "Noah", "Olivia", "Priya",
    "Raj", "Sofia", "Thomas", "William", "Zara",
)
LAST_NAMES = (
    "Anderson", "Bennett", "Brown", "Campbell", "Carter", "Das", "Evans",
    "Fischer", "Gupta", "Harris", "Joshi", "Khan", "Kumar", "Lewis",
    "Martin", "Miller", "Patel", "Roberts", "Schmidt", "Shah", "Singh",
    "Taylor", "Thompson", "Walker", "Wilson",
)

# Each title is paired with a level so salary bands remain appropriate across countries.
JOB_TITLES = {
    "Engineering": (("Software Engineer", 2), ("Senior Software Engineer", 4), ("Engineering Manager", 5)),
    "Product": (("Product Analyst", 2), ("Product Manager", 4), ("Senior Product Manager", 5)),
    "Finance": (("Financial Analyst", 2), ("Finance Manager", 5), ("Controller", 6)),
    "Human Resources": (("HR Specialist", 2), ("HR Business Partner", 4), ("HR Manager", 5)),
    "Sales": (("Sales Representative", 2), ("Account Executive", 4), ("Sales Manager", 5)),
    "Marketing": (("Marketing Specialist", 2), ("Marketing Manager", 5), ("Brand Director", 6)),
    "Operations": (("Operations Analyst", 2), ("Operations Manager", 5), ("Director of Operations", 6)),
    "Legal": (("Legal Counsel", 4), ("Senior Legal Counsel", 5), ("Legal Director", 6)),
    "Customer Support": (("Support Specialist", 1), ("Support Lead", 3), ("Support Manager", 5)),
}

# Annual salary bands in each country's local currency, indexed by career level.
SALARY_BANDS = {
    "India": (480_000, 900_000, 1_500_000, 2_400_000, 3_600_000, 5_000_000),
    "United States": (42_000, 65_000, 90_000, 125_000, 160_000, 220_000),
    "United Kingdom": (28_000, 42_000, 60_000, 82_000, 110_000, 150_000),
    "Germany": (38_000, 52_000, 72_000, 95_000, 125_000, 170_000),
    "Canada": (45_000, 62_000, 85_000, 115_000, 145_000, 190_000),
    "Australia": (55_000, 75_000, 100_000, 135_000, 170_000, 220_000),
}


def _salary_value(rng: random.Random, country: str, level: int) -> Decimal:
    low = SALARY_BANDS[country][level - 1]
    high = SALARY_BANDS[country][level - 1] * 1.18
    amount = rng.uniform(low, high)
    return Decimal(str(round(amount / 100) * 100)).quantize(Decimal("0.01"))


def generate_seed_data(
    count: int = SEED_SIZE,
    *,
    random_seed: int = DEFAULT_SEED,
    effective_from: date = DEFAULT_EFFECTIVE_FROM,
) -> list[dict[str, Any]]:
    """Generate employee and current-salary payloads without database access."""
    if count < 0:
        raise ValueError("count must not be negative")

    rng = random.Random(random_seed)
    created_at = DEFAULT_CREATED_AT
    rows: list[dict[str, Any]] = []

    for number in range(1, count + 1):
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        country = rng.choice(COUNTRIES)
        department = rng.choice(DEPARTMENTS)
        job_title, level = rng.choice(JOB_TITLES[department])
        employee_code = f"EMP{number:05d}"
        email = f"{first_name.lower()}.{last_name.lower()}.{number:05d}@acme.example.com"
        base_salary = _salary_value(rng, country, level)

        rows.append(
            {
                "employee": {
                    "employee_code": employee_code,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "country": country,
                    "department": department,
                    "job_title": job_title,
                    "status": "active",
                    "created_at": created_at,
                    "updated_at": created_at,
                },
                "salary": {
                    "base_salary": base_salary,
                    "bonus": (base_salary * Decimal("0.10")).quantize(Decimal("0.01")),
                    "currency": COUNTRY_CURRENCIES[country],
                    "effective_from": effective_from,
                    "effective_to": None,
                    "reason": "Initial salary",
                    "created_at": created_at,
                    "updated_at": created_at,
                },
            }
        )

    return rows


def seed_database(
    count: int = SEED_SIZE,
    *,
    session_factory: Callable[[], Session] | None = None,
) -> int:
    """Insert missing seeded employees and their current salaries atomically.

    Employee codes in the seed range are treated as owned by this seed. Existing
    codes are skipped, so rerunning the command does not duplicate data.
    """
    if session_factory is None:
        from app.db.session import SessionLocal

        session_factory = SessionLocal

    rows = generate_seed_data(count)
    codes = [row["employee"]["employee_code"] for row in rows]

    try:
        with session_factory() as session:
            with session.begin():
                existing_codes = set(
                    session.scalars(
                        select(Employee.employee_code).where(
                            Employee.employee_code.in_(codes)
                        )
                    )
                )
                pending_rows = [
                    row for row in rows
                    if row["employee"]["employee_code"] not in existing_codes
                ]

                if not pending_rows:
                    return 0

                session.execute(
                    insert(Employee),
                    [row["employee"] for row in pending_rows],
                )
                inserted_codes = [
                    row["employee"]["employee_code"] for row in pending_rows
                ]
                inserted_employees = session.execute(
                    select(Employee.id, Employee.employee_code).where(
                        Employee.employee_code.in_(inserted_codes)
                    )
                )
                employee_ids = {
                    code: employee_id
                    for employee_id, code in inserted_employees
                }
                session.execute(
                    insert(SalaryRecord),
                    [
                        {
                            **row["salary"],
                            "employee_id": employee_ids[
                                row["employee"]["employee_code"]
                            ],
                        }
                        for row in pending_rows
                    ],
                )
                return len(pending_rows)
    except SQLAlchemyError as exc:
        raise RuntimeError(
            "Unable to seed salary data; verify that the database is available "
            "and migrations have been applied."
        ) from exc


def main() -> None:
    try:
        inserted = seed_database()
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc
    print(f"Seed complete: inserted {inserted} employees and {inserted} current salaries.")


if __name__ == "__main__":
    main()