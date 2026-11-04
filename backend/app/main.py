from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes import router as health_router
from backend.app.api.operations import router as operations_router
from backend.app.api.customer_routes import router as legacy_customer_router
from backend.app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Plataforma de gestão logística OMNILOG HUB.",
)

app.include_router(health_router)
app.include_router(operations_router)
app.include_router(legacy_customer_router)

FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
