"""
Intent Classifier Agent
Classifies user intent and extracts entities from messages
"""

import logging
import os
from typing import Dict, Any, Optional
from openai import AzureOpenAI
from azure.functions import HttpRequest, HttpResponse
import json

logger = logging.getLogger(__name__)


class IntentClassifierAgent:
    """
    Classifies user intent using Azure OpenAI GPT-4.
    """
    
    INTENT_CATEGORIES = [
        "LEAVE_REQUEST",
        "POLICY_QUESTION",
        "EMPLOYEE_DATA",
        "BENEFITS_QUERY",
        "ESCALATION",
        "UNKNOWN"
    ]
    
    def __init__(self):
        """Initialize the intent classifier with Azure OpenAI."""
        self.client = AzureOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            api_version=os.getenv("OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME", "gpt-4")
    
    async def classify(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Classify user intent from a message.
        
        Args:
            message: User's input message
            context: Optional conversation context
            
        Returns:
            Dictionary with intent, confidence, and entities
        """
        system_prompt = f"""You are an HR Service Desk intent classifier.
Your job is to classify user requests into one of these categories:
{', '.join(self.INTENT_CATEGORIES)}

Return a JSON object with:
- intent: One of the categories above
- confidence: A score between 0 and 1
- entities: Extracted entities (dates, employee IDs, policy names, etc.)
- requires_clarification: Boolean indicating if more info is needed

Be precise and confident in your classification."""

        user_prompt = f"User message: {message}"
        if context:
            user_prompt += f"\nContext: {json.dumps(context)}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validate result
            if result.get("intent") not in self.INTENT_CATEGORIES:
                result["intent"] = "UNKNOWN"
            
            logger.info(f"Intent classified: {result.get('intent')} (confidence: {result.get('confidence')})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error classifying intent: {str(e)}")
            return {
                "intent": "UNKNOWN",
                "confidence": 0.0,
                "entities": {},
                "requires_clarification": True,
                "error": str(e)
            }


# Azure Function entry point
async def main(req: HttpRequest) -> HttpResponse:
    """
    Azure Function HTTP trigger for intent classifier agent.
    """
    try:
        body = req.get_json()
        message = body.get("message")
        context = body.get("context")
        
        classifier = IntentClassifierAgent()
        result = await classifier.classify(message, context)
        
        return HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logger.error(f"Error in intent classifier: {str(e)}")
        return HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )

