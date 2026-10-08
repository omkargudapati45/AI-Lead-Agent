from sqlalchemy.orm import Session
from app.models.lead import Lead, LeadHistory
from app.schemas.lead import LeadCreate, LeadUpdate
import logging

logger = logging.getLogger(__name__)

def create_lead(db: Session, lead: LeadCreate) -> Lead:
    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    # Log the history
    log_history(db, db_lead.id, "LEAD_CREATED", "Lead was manually created via API.")
    return db_lead

def get_leads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Lead).order_by(Lead.created_at.desc()).offset(skip).limit(limit).all()

def get_lead(db: Session, lead_id: int):
    return db.query(Lead).filter(Lead.id == lead_id).first()

def update_lead(db: Session, lead_id: int, lead_update: LeadUpdate) -> Lead:
    db_lead = get_lead(db, lead_id)
    if not db_lead:
        return None
    
    update_data = lead_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_lead, key, value)
        
    db.commit()
    db.refresh(db_lead)
    return db_lead

def delete_lead(db: Session, lead_id: int):
    db_lead = get_lead(db, lead_id)
    if db_lead:
        db.delete(db_lead)
        db.commit()
    return db_lead

def log_history(db: Session, lead_id: int, action: str, notes: str = None):
    history_entry = LeadHistory(lead_id=lead_id, action=action, notes=notes)
    db.add(history_entry)
    db.commit()

def get_lead_history(db: Session, lead_id: int):
    return db.query(LeadHistory).filter(LeadHistory.lead_id == lead_id).order_by(LeadHistory.created_at.desc()).all()
