from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Lead, LeadHistory
from app.api.leads import router as leads_router

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Lead Agent API",
    description="API for managing and analyzing incoming leads.",
    version="1.0.0"
)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leads_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Lead Agent API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
