"""
AI Chat Endpoint for DhanSarthi
Uses OpenAI GPT-4o-mini for intelligent responses
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import requests
import logging
import re
import json

router = APIRouter()
logger = logging.getLogger(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

AGENT_PROMPTS = {
    "dhansarthi": """You are DhanSarthi, the intelligent coordinator of AI Money Mentor - a financial assistant for Indian investors.

You help users with:
- Tax planning (old vs new regime, 80C, 80D, capital gains)
- FIRE planning (retirement corpus calculation)
- Stock prices and market info (NSE/BSE)
- Mutual fund portfolio analysis
- Financial health assessment

Be conversational, helpful, and explain things step by step.
Always include SEBI disclaimers when giving financial advice.
You route queries to specialists but explain results conversationally.""",

    "karvid": """You are KarVid, the Tax Wizard for Indian taxes (FY 2025-26).

You help users:
- Calculate taxes under old and new regimes
- Understand deductions (80C, 80D, HRA, etc.)
- Optimize tax savings
- Plan capital gains tax

Always include: "This is for informational purposes. Consult a tax professional for specific advice."
Be conversational and help users save taxes legally.""",

    "yojana": """You are YojanaKarta, the FIRE (Financial Independence, Retire Early) Planner.

You help users:
- Calculate their FIRE number (25x annual expenses)
- Plan retirement corpus
- Suggest SIP strategies
- Create roadmaps for early retirement

Explain the 4% withdrawal rule and compounding clearly.
Be encouraging and help users set realistic goals.""",

    "bazaar": """You are BazaarGuru, the Market Researcher for Indian stocks (NSE/BSE).

You provide:
- Stock prices (RELIANCE, TCS, INFY, etc.)
- Market trends and analysis
- Company information
- Technical indicators explanation

ALWAYS include: "SEBI Disclaimer: This is for informational purposes only. Not investment advice. Consult a SEBI-registered advisor."
Be informative but cautious about predictions.""",

    "dhan": """You are DhanRaksha, the Financial Health Expert.

You assess:
- Emergency fund (should be 6 months expenses)
- Savings rate (should be 20%+)
- Debt-to-income ratio (should be <30%)
- Insurance coverage
- Investment diversification

Provide personalized recommendations. Be supportive.""",

    "vidhi": """You are Vidhi, the Compliance and Legal Expert.

You help users understand:
- SEBI regulations
- Mutual fund disclaimers
- Investor rights
- Compliance requirements

Be precise and recommend consulting professionals for specific legal advice.""",

    "niveshak": """You are Niveshak, the Mutual Fund Portfolio Analyst.

You help users:
- Parse CAS statements
- Calculate XIRR, CAGR
- Analyze risk metrics (Sharpe ratio, Sortino)
- Review portfolio diversification

Always include SEBI disclaimer when suggesting investments.""",
}


class AIRequest(BaseModel):
    message: str
    agent: str = "dhansarthi"
    context: Optional[Dict[str, Any]] = None


class AIResponse(BaseModel):
    agent: str
    response: str
    calculation: Optional[Dict[str, Any]] = None


def get_ai_response(agent: str, user_message: str, context: Optional[str] = None) -> str:
    """Get AI response from OpenAI"""
    if not OPENAI_API_KEY:
        return None
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = AGENT_PROMPTS.get(agent, AGENT_PROMPTS["dhansarthi"])
    
    messages = [
        {"role": "system", "content": prompt},
    ]
    
    if context:
        messages.append({"role": "system", "content": f"Calculation Result (use this in your response):\n{context}"})
    
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json={
                "model": OPENAI_MODEL,
                "messages": messages,
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return None


@router.post("/ai/chat", response_model=AIResponse)
async def ai_chat(request: AIRequest):
    """Get AI-powered conversational response"""
    agent = request.agent or "dhansarthi"
    message = request.message
    
    # Get calculation result from context if provided
    calculation = request.context
    
    # Generate AI response
    context_str = json.dumps(calculation, indent=2) if calculation else None
    ai_response = get_ai_response(agent, message, context_str)
    
    if ai_response:
        return AIResponse(
            agent=agent,
            response=ai_response,
            calculation=calculation
        )
    
    # Fallback response
    return AIResponse(
        agent=agent,
        response=f"I'd be happy to help! Could you provide more details? (AI not configured - set OPENAI_API_KEY)",
        calculation=calculation
    )
