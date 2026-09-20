# Performance Verification

The backend uses database-side pagination and aggregation:

- Employee listing applies `WHERE`, `ORDER BY`, `OFFSET`, and `LIMIT` in SQL.
- Analytics uses `COUNT`, `AVG`, `SUM`, and `GROUP BY` in SQL.
- No employee or salary collection is loaded before pagination or aggregation.

## Seed verification

With `DATABASE_URL` configured and migrations applied, run from `backend`:

```powershell
python -m app.seed
python -m scripts.verify_seed
python -m app.seed
python -m scripts.verify_seed
```

The verification script checks the managed `EMP00001`-`EMP10000` seed range:
10,000 employees, unique employee codes and emails, at least one salary record
per seeded employee, and exactly 10,000 current salary records. It also prints
total table counts so unrelated application data and salary history remain
visible but are not treated as a seed failure. Running the seed a second time
should leave the seed-range counts unchanged.

## Representative measurements

Run against the seeded database:

```powershell
python -m scripts.measure_performance --repeats 5
```

The script measures employee page 1 with 25 rows, employee-code search,
country filtering, department filtering, compensation summary, country
analytics, department analytics, and salary distribution. It prints average and
minimum wall-clock time in milliseconds for the local environment. These values
are diagnostic measurements, not fixed performance thresholds.

## Index review

Existing indexes cover the frequent access paths:

- `employees.employee_code`, `email`, `country`, `department`, and `status`
- `salary_records.employee_id` and `effective_from`
- The unique partial current-salary index on `employee_id` where `effective_to IS NULL`

No additional index was added because the current query patterns are already
covered and adding an index on every analytics grouping column would increase
write cost without a measured need.