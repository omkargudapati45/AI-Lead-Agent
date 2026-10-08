from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse, LeadHistoryResponse
from app.crud import lead as crud_lead
from app.agent.workflow import analyze_lead_workflow

router = APIRouter(
    prefix="/leads",
    tags=["leads"],
)

@router.post("/", response_model=LeadResponse)
def create_lead(lead: LeadCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Create a new lead and trigger the AI analysis workflow in the background.
    """
    # 1. Save lead to database immediately
    db_lead = crud_lead.create_lead(db=db, lead=lead)
    
    # 2. Add AI analysis to the background task queue
    background_tasks.add_task(analyze_lead_workflow, db_lead.id)
    
    # 3. Return the new lead to the user immediately without waiting for AI
    return db_lead

@router.get("/", response_model=List[LeadResponse])
def read_leads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all leads with pagination.
    """
    return crud_lead.get_leads(db, skip=skip, limit=limit)

@router.get("/{lead_id}", response_model=LeadResponse)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    Get a single lead by ID.
    """
    db_lead = crud_lead.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db)):
    """
    Update a lead (e.g., human-in-the-loop changing status or priority).
    """
    db_lead = crud_lead.update_lead(db, lead_id=lead_id, lead_update=lead_update)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Log that a manual update happened
    crud_lead.log_history(db, lead_id, "LEAD_UPDATED", "Lead was updated via API.")
    return db_lead

@router.delete("/{lead_id}")
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    Delete a lead.
    """
    db_lead = crud_lead.delete_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead deleted successfully"}

@router.get("/{lead_id}/history", response_model=List[LeadHistoryResponse])
def get_lead_history(lead_id: int, db: Session = Depends(get_db)):
    """
    Get the audit trail / history for a single lead.
    """
    return crud_lead.get_lead_history(db, lead_id=lead_id)
