from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import leads, forms, ai
from .database import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Marketing Automation API",
    description="API for AI-Driven Hyper-Personalized Marketing Automation System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/api", tags=["leads"])
app.include_router(forms.router, prefix="/api", tags=["forms"])
app.include_router(ai.router, prefix="/api", tags=["ai"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Marketing Automation API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }
