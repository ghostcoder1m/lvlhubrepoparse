from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import leads, campaigns, automation
from app.database import Base, engine
from app.worker import start_automation_worker

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Marketing Automation API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)
app.include_router(campaigns.router)
app.include_router(automation.router)

@app.on_event("startup")
def startup_event():
    """Start background tasks on application startup."""
    start_automation_worker()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Marketing Automation API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    } 