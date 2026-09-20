import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.employees import router as employee_router
from app.api.analytics import router as analytics_router
from app.api.salary import router as salary_router


def get_cors_origins() -> list[str]:
    raw = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["http://localhost:5173"]


app = FastAPI(title="ACME Salary Management API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(employee_router)
app.include_router(salary_router)
app.include_router(analytics_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )