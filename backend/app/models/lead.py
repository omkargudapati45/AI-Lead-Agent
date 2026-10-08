from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    FOLLOW_UP_SCHEDULED = "FOLLOW_UP_SCHEDULED"
    CONVERTED = "CONVERTED"
    DISCARDED = "DISCARDED"

class LeadPriority(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    UNASSIGNED = "UNASSIGNED"

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=True)
    email = Column(String, index=True, nullable=True)
    phone = Column(String, index=True, nullable=True)
    company = Column(String, nullable=True)
    source = Column(String, default="Manual") # e.g., Website, Email, WhatsApp
    
    # Original message from the lead
    message = Column(Text, nullable=False)
    
    # AI Extracted Data
    intent = Column(String, nullable=True) # e.g., Purchase Inquiry, Support, Spam
    requirement_summary = Column(Text, nullable=True) 
    
    # System fields
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    priority = Column(Enum(LeadPriority), default=LeadPriority.UNASSIGNED)
    
    # AI generated drafted response and recommended action
    draft_response = Column(Text, nullable=True)
    recommended_action = Column(String, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class LeadHistory(Base):
    __tablename__ = "lead_history"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, index=True)
    action = Column(String, nullable=False) # e.g., "AI_ANALYSIS_COMPLETED", "HUMAN_APPROVED_RESPONSE"
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
