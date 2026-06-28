from fastapi import FastAPI
from crm_analytics.api.routes.dashboard import router as dashboard_router
from crm_analytics.api.routes.performance import router as performance_router

app = FastAPI(title="CRM Analytics API", version="1.0.0")
app.include_router(dashboard_router)
app.include_router(performance_router)

@app.get("/health")
def health():
    return {"status": "ok"}
