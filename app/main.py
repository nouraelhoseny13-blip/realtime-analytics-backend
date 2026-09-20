import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app import models

from app.api.routes.analytics import router as analytics_router
from app.api.routes.auth import router as auth_router
from app.api.routes.activity import router as activity_router
from app.api.routes.notifications import router as notifications_router
from app.api.routes.websocket import router as websocket_router


load_dotenv()


FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:5173",
)


ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://realtime-analytics-dashboard-theta.vercel.app",
]


ALLOWED_ORIGINS = list(dict.fromkeys(ALLOWED_ORIGINS))


app = FastAPI(
    title="Real-Time Analytics API",
    version="1.0.0",
)


@app.on_event("startup")
def create_database_tables():
    Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(analytics_router)
app.include_router(auth_router)
app.include_router(activity_router)
app.include_router(notifications_router)
app.include_router(websocket_router)


@app.get("/")
def root():
    return {
        "message": "Real-Time Analytics API is running",
        "status": "ok",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "realtime-analytics-backend",
    }