# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.services.monitoring import start_monitoring
from app.helpers.ai_helpers import create_ai_team, run_ai_tasks
import logging

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Create AI team
ai_team = create_ai_team()

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting up CostByte backend...")
    
    # Start monitoring service
    start_monitoring()
    
    # Start AI tasks
    run_ai_tasks(ai_team)
    
    logger.info("CostByte backend started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down CostByte backend...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CostByte API is running",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
