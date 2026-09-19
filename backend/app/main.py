from fastapi import FastAPI


app = FastAPI(title="ACME Salary Management API")


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}