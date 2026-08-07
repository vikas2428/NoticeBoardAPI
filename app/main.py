from fastapi import FastAPI

from app.database.database import database
from app.utils.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Notice Board Management API"
)


@app.on_event("startup")
def startup():
    database.create_tables()
    print("✅ Database initialized successfully.")


@app.get("/")
async def home():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "Connected",
        "status": "Running"
    }