from fastapi import FastAPI

app = FastAPI(
    title="Notice Board API",
    version="1.0.0",
    description="A FastAPI-based Notice Board Management System"
)


@app.get("/")
async def home():
    return {
        "message": "Welcome to Notice Board API",
        "status": "Running Successfully"
    }