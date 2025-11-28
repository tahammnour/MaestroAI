"""
MaestroAI REST API
FastAPI application for HR Service Desk
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="MaestroAI HR Service Desk API",
    description="Multi-agent HR Service Desk automation API",
    version="1.0.0"
)


class ServiceRequest(BaseModel):
    """Service request model."""
    message: str
    user_id: str
    context: Optional[Dict[str, Any]] = None


class ServiceResponse(BaseModel):
    """Service response model."""
    intent: str
    confidence: float
    answer: str
    knowledge_used: Optional[Dict[str, Any]] = None
    runbook_executed: bool = False
    escalated: bool = False
    explanation: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "MaestroAI HR Service Desk API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "openai": "connected",
            "cosmos": "connected",
            "search": "connected"
        }
    }


@app.post("/api/process", response_model=ServiceResponse)
async def process_request(request: ServiceRequest):
    """
    Process a service desk request through the multi-agent system.
    
    Args:
        request: Service request with user message and context
        
    Returns:
        ServiceResponse with processed result
    """
    try:
        # TODO: Call orchestrator agent
        # For now, return a mock response
        return ServiceResponse(
            intent="LEAVE_REQUEST",
            confidence=0.95,
            answer="Your leave request has been processed. I've checked your leave balance and policy compliance.",
            knowledge_used={"policies": ["Sick Leave Policy"]},
            runbook_executed=True,
            escalated=False,
            explanation="The system classified your request as a leave request, retrieved relevant policies, and executed the leave request runbook."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/intents")
async def list_intents():
    """List all supported intent categories."""
    return {
        "intents": [
            "LEAVE_REQUEST",
            "POLICY_QUESTION",
            "EMPLOYEE_DATA",
            "BENEFITS_QUERY",
            "ESCALATION",
            "UNKNOWN"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

