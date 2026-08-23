from fastapi.responses import FileResponse
import time

from fastapi import FastAPI

from app.database.database import database
from app.utils.config import settings
from app.routes.notice import router as notice_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Notice Board Management API"
)


@app.middleware("http")
async def request_logging_middleware(request, call_next):
    """
    Log every HTTP request and its processing time.
    """

    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    print(
        f"[MIDDLEWARE] "
        f"{request.method} "
        f"{request.url.path} "
        f"completed in "
        f"{process_time:.6f} seconds"
    )

    response.headers["X-Process-Time"] = str(process_time)

    return response


app.include_router(
    notice_router,
    prefix="/api",
    tags=["Notices"]
)


@app.on_event("startup")
def startup():
    database.create_tables()


@app.get("/")
async def home():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": "Connected",
        "status": "Running"
    }

@app.get("/dashboard", include_in_schema=False)
async def dashboard():
    return FileResponse("app/frontend/index.html")