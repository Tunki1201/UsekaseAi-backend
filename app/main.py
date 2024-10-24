from fastapi import FastAPI
from app.views import (
    account_view,
    api_usage_view,
    audit_log_view,
    chapter_view,
    error_log_view,
    notification_view,
    payments_view,
    report_view,
    scraped_data_view,
)
from app.views.user_view import router as user_router

from app.db import engine, Base
from fastapi.middleware.cors import CORSMiddleware  # If you need CORS support
import uvicorn

# Create FastAPI app instance
app = FastAPI()

# CORS middleware to allow all origins (if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event handler to create database tables on startup
@app.on_event("startup")
async def startup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Include routers
app.include_router(scraped_data_view.router)
app.include_router(error_log_view.router)
app.include_router(notification_view.router)
app.include_router(chapter_view.router)
app.include_router(api_usage_view.router)
app.include_router(audit_log_view.router)
app.include_router(payments_view.router)
app.include_router(account_view.router)
app.include_router(user_router, prefix="/api")
app.include_router(report_view.router, prefix="/api")

# If running this script directly, start Uvicorn server
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
