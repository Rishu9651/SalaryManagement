from __future__ import annotations

import argparse
import time
from collections.abc import Callable

from app.db.session import SessionLocal
from app.repositories.analytics import (
    get_compensation_by_currency,
    get_compensation_by_dimension,
)
from app.repositories.employee import get_employee_page
from app.services.analytics import get_distribution


def measure(label: str, operation: Callable[[], object], repeats: int) -> None:
    durations = []
    for _ in range(repeats):
        started = time.perf_counter()
        operation()
        durations.append((time.perf_counter() - started) * 1000)

    average = sum(durations) / len(durations)
    print(f"{label:24} average={average:8.2f} ms min={min(durations):8.2f} ms")


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure representative analytics queries.")
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be at least 1")

    with SessionLocal() as session:
        measure(
            "employee list",
            lambda: get_employee_page(session, 1, 25, None, None, None),
            args.repeats,
        )
        measure(
            "employee search",
            lambda: get_employee_page(session, 1, 25, "EMP00001", None, None),
            args.repeats,
        )
        measure(
            "country filter",
            lambda: get_employee_page(session, 1, 25, None, "India", None),
            args.repeats,
        )
        measure(
            "department filter",
            lambda: get_employee_page(session, 1, 25, None, None, "Engineering"),
            args.repeats,
        )
        measure(
            "compensation summary",
            lambda: get_compensation_by_currency(session),
            args.repeats,
        )
        measure(
            "country analytics",
            lambda: get_compensation_by_dimension(session, "country"),
            args.repeats,
        )
        measure(
            "department analytics",
            lambda: get_compensation_by_dimension(session, "department"),
            args.repeats,
        )
        measure(
            "salary distribution",
            lambda: get_distribution(session),
            args.repeats,
        )


if __name__ == "__main__":
    main()