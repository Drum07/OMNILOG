from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from backend.app.db.session import engine

router = APIRouter()

@router.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok", "application": "OMNILOG HUB"}

@router.get("/health/db", tags=["Sistema"])
def database_health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except SQLAlchemyError:
        return {"status": "error", "database": "unavailable"}
