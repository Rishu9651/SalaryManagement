from fastapi import FastAPI

from app.api.employees import router as employee_router
from app.api.salary import router as salary_router


app = FastAPI(title="ACME Salary Management API")
app.include_router(employee_router)
app.include_router(salary_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}