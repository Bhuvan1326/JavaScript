"""
AI Responder for DhanSarthi
Uses OpenAI GPT-4o-mini for intelligent responses
"""

import os
from typing import Optional, Dict, Any
import requests
import logging

logger = logging.getLogger(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

AGENT_PROMPTS = {
    "dhansarthi": """You are DhanSarthi, the intelligent coordinator of AI Money Mentor.
You route financial queries and explain things conversationally.
You're helpful, knowledgeable about Indian finance, and guide users step by step.
Respond in a friendly, conversational manner. Be concise but thorough.""",

    "karvid": """You are KarVid, the Tax Wizard for Indian taxes (FY 2025-26).
Help users understand taxes under both old and new regimes.
Explain deductions (80C, 80D, HRA), capital gains, and tax optimization.
Always include SEBI disclaimer when giving tax advice.
Be conversational and help users save taxes legally.""",

    "niveshak": """You are Niveshak, the Mutual Fund Portfolio Analyst.
Help users analyze MF portfolios, calculate XIRR, and understand risk metrics.
Explain Sharpe ratio, Sortino ratio, and CAGR in simple terms.
Always include SEBI disclaimer when suggesting investments.""",

    "yojana": """You are YojanaKarta, the FIRE Planner.
Help users plan financial independence and early retirement.
Calculate FIRE numbers, suggest SIP strategies, create retirement roadmaps.
Explain the 4% rule and compounding. Be encouraging.""",

    "bazaar": """You are BazaarGuru, the Market Researcher.
Provide stock prices, market analysis, and company information for NSE/BSE stocks.
Explain technical indicators and market trends in simple terms.
Always include SEBI disclaimer - this is NOT investment advice.""",

    "dhan": """You are DhanRaksha, the Financial Health Expert.
Assess users' financial health based on emergency fund, savings rate, debt-to-income, etc.
Provide personalized recommendations. Be supportive.""",

    "vidhi": """You are Vidhi, the Legal and Compliance Expert.
Help users understand SEBI regulations, mutual fund disclaimers, and investor rights.
Be precise and always recommend consulting a professional for specific legal advice.""",
}


def get_ai_response(agent: str, user_message: str, context: Optional[str] = None) -> str:
    """Get AI response from OpenAI"""
    if not OPENAI_API_KEY:
        # Fallback to calculation-based response
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
        messages.append({"role": "system", "content": f"Calculation Result: {context}"})
    
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


def generate_response_with_ai(agent: str, user_message: str, calculation_result: Optional[Dict] = None) -> str:
    """Generate response using AI + calculation results"""
    context = None
    if calculation_result:
        import json
        context = json.dumps(calculation_result, indent=2)
    
    ai_response = get_ai_response(agent, user_message, context)
    
    if ai_response:
        return ai_response
    
    # Fallback to calculation result if AI fails
    if calculation_result:
        return format_calculation_result(agent, calculation_result)
    
    return "I'd be happy to help! Could you provide more details?"


def format_calculation_result(agent: str, result: Dict) -> str:
    """Format calculation result as fallback"""
    # This is called when AI is not available
    if agent == "karvid":
        return f"**Tax Calculation**\n\nTotal Tax: ₹{result.get('total_tax', 0):,.0f}\nEffective Rate: {result.get('effective_rate', 0)}%\nRegime: {result.get('regime', 'new').upper()}"
    elif agent == "yojana":
        return f"**FIRE Number**\n\nClassic FIRE: ₹{result.get('classic_fire', 0)/10000000:.2f} Cr\nFat FIRE: ₹{result.get('fat_fire', 0)/10000000:.2f} Cr\nMonthly Withdrawal: ₹{result.get('monthly_expenses', 0):,}"
    elif agent == "bazaar":
        return f"**Stock Quote**\n\n{result.get('symbol', 'N/A')}: ₹{result.get('price', 0):,.0f}\nChange: {result.get('change_percent', 0):.2f}%"
    elif agent == "dhan":
        return f"**Financial Health Score**\n\nScore: {result.get('overall_score', 0)}/100\nGrade: {result.get('grade', 'N/A')}"
    return str(result)
