import os
import json
import logging
from pydantic import BaseModel
from google import genai
from google.genai import types
from app.database import SessionLocal
from app.crud.lead import get_lead, update_lead, log_history
from app.schemas.lead import LeadUpdate
from app.models.lead import LeadStatus, LeadPriority
from app.agent.prompts import LEAD_ANALYSIS_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

# Define the exact structure we want the AI to return
class AIAnalysisResult(BaseModel):
    intent: str
    requirement_summary: str
    priority: LeadPriority
    draft_response: str
    recommended_action: str

def analyze_lead_workflow(lead_id: int):
    """
    Background task to analyze a newly created lead using Gemini AI.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY not found in environment. Skipping AI analysis.")
        return

    # Create an isolated database session for this background task
    db = SessionLocal()
    try:
        db_lead = get_lead(db, lead_id)
        if not db_lead:
            logger.error(f"Lead {lead_id} not found for AI analysis.")
            return

        # Initialize the Gemini Client
        client = genai.Client(api_key=api_key)
        
        # Construct the user message
        user_message = f"""
Lead Information:
- Name: {db_lead.name or 'Unknown'}
- Company: {db_lead.company or 'Unknown'}
- Source: {db_lead.source}

Original Message:
"{db_lead.message}"
"""
        logger.info(f"Starting AI Analysis for Lead {lead_id}...")

        # Call Gemini with Structured Outputs
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=LEAD_ANALYSIS_SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=AIAnalysisResult,
                temperature=0.2, # Low temperature for more deterministic classification
            ),
        )

        # Parse the JSON response into our Pydantic model
        result_json = response.text
        analysis = AIAnalysisResult.model_validate_json(result_json)

        # Map AI results to LeadUpdate schema
        update_data = LeadUpdate(
            intent=analysis.intent,
            requirement_summary=analysis.requirement_summary,
            priority=analysis.priority,
            draft_response=analysis.draft_response,
            recommended_action=analysis.recommended_action,
            status=LeadStatus.NEW  # Keeps it as NEW so human knows to review it
        )

        # Save to database
        update_lead(db, lead_id, update_data)
        
        # Log history
        log_history(
            db=db, 
            lead_id=lead_id, 
            action="AI_ANALYSIS_COMPLETED", 
            notes=f"AI classified intent as '{analysis.intent}' with priority {analysis.priority.value}."
        )
        logger.info(f"Successfully completed AI Analysis for Lead {lead_id}.")
        
    except Exception as e:
        logger.error(f"Failed to analyze lead {lead_id}: {str(e)}")
        log_history(
            db=db, 
            lead_id=lead_id, 
            action="AI_ANALYSIS_FAILED", 
            notes=f"Error: {str(e)}"
        )
    finally:
        db.close()
