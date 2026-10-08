from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.lead import LeadStatus, LeadPriority

class LeadBase(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: str = "Manual"
    message: str

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    status: Optional[LeadStatus] = None
    priority: Optional[LeadPriority] = None
    intent: Optional[str] = None
    requirement_summary: Optional[str] = None
    draft_response: Optional[str] = None
    recommended_action: Optional[str] = None

class LeadResponse(LeadBase):
    id: int
    intent: Optional[str] = None
    requirement_summary: Optional[str] = None
    status: LeadStatus
    priority: LeadPriority
    draft_response: Optional[str] = None
    recommended_action: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class LeadHistoryBase(BaseModel):
    action: str
    notes: Optional[str] = None

class LeadHistoryResponse(LeadHistoryBase):
    id: int
    lead_id: int
    created_at: datetime

    class Config:
        from_attributes = True
