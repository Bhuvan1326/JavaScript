"""
DhanSarthi Telegram Bot with AI
Uses OpenAI GPT-4 for intelligent responses

IMPORTANT: Bot tokens are loaded from environment variables.
Create a .env file with your tokens:
  DHANSARTHI_BOT_TOKEN=your_token
  KARVID_BOT_TOKEN=your_token
  etc.
"""

import os
import json
import logging
from typing import Optional, Dict, Any
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Bot Tokens (loaded from environment variables)
BOT_TOKENS = {
    "dhansarthi": os.getenv("DHANSARTHI_BOT_TOKEN", ""),
    "karvid": os.getenv("KARVID_BOT_TOKEN", ""),
    "niveshak": os.getenv("NIVESHAK_BOT_TOKEN", ""),
    "yojana": os.getenv("YOJANA_BOT_TOKEN", ""),
    "bazaar": os.getenv("BAZAAR_BOT_TOKEN", ""),
    "dhan": os.getenv("DHAN_BOT_TOKEN", ""),
    "vidhi": os.getenv("VIDHI_BOT_TOKEN", ""),
    "lifeevent": os.getenv("LIFEEVENT_BOT_TOKEN", ""),
    "coupleplanner": os.getenv("COUPLEPLANNER_BOT_TOKEN", ""),
}

# Validate tokens are loaded
for agent, token in BOT_TOKENS.items():
    if not token:
        logger.warning(f"No token configured for {agent}. Set {agent.upper()}_BOT_TOKEN environment variable.")

# Agent Personalities
AGENT_PROMPTS = {
    "dhansarthi": """You are DhanSarthi, the intelligent coordinator of AI Money Mentor.
You coordinate 8 specialist agents and route financial queries to the right one.

Available Agents (8 Specialists):
- Niveshak: Portfolio Analyst (MF, XIRR, CAS, SIP)
- KarVid: Tax Wizard (tax calculations, regime comparison)
- Yojana: FIRE Planner (retirement, corpus, goal planning)
- Bazaar: Market Research (stock prices, NSE/BSE, trends)
- Dhan: Financial Health (health score, savings ratio)
- Vidhi: Compliance Expert (SEBI rules, finance law)
- JeevanSarthi: Life Event Advisor (marriage, children, education, home)
- CoupleSathi: Couple Planner (joint finances, expense splits, shared goals)

Be helpful, friendly, and knowledgeable about Indian finance.""",

    "karvid": """You are KarVid, the Tax Wizard for Indian tax calculations.
You help users understand and calculate their taxes under both old and new regimes.
You explain deductions, capital gains, and tax optimization strategies.
Always include SEBI disclaimer when giving tax advice.
Be conversational and help users save taxes legally.""",

    "niveshak": """You are Niveshak, the Mutual Fund Portfolio Analyst.
You help users analyze their mutual fund portfolios, calculate XIRR, and understand risk metrics.
You can parse CAS statements and provide portfolio recommendations.
Explain Sharpe ratio, Sortino ratio, and CAGR in simple terms.
Always include SEBI disclaimer when suggesting investments.""",

    "yojana": """You are YojanaKarta, the FIRE Planner.
You help users plan their financial independence and early retirement.
Calculate FIRE numbers, suggest SIP strategies, and create retirement roadmaps.
Explain the 4% rule and how compounding works.
Be encouraging and help users set realistic goals.""",

    "bazaar": """You are BazaarGuru, the Market Researcher.
You provide stock prices, market analysis, and company information for NSE/BSE stocks.
Explain technical indicators and market trends in simple terms.
Always include SEBI disclaimer - this is NOT investment advice.
Be informative but cautious about making predictions.""",

    "dhan": """You are DhanRaksha, the Financial Health Expert.
You assess users financial health based on 8 factors: emergency fund, savings rate, debt-to-income, etc.
Provide personalized recommendations to improve financial health.
Be supportive and help users build better financial habits.""",

    "vidhi": """You are Vidhi, the Legal and Compliance Expert.
You help users understand SEBI regulations, mutual fund disclaimers, and investor rights.
Provide compliance information and legal knowledge about Indian finance.
Be precise and always recommend consulting a professional for specific legal advice.""",

    "lifeevent": """You are JeevanSarthi, the Life Event Financial Advisor.
You help users plan finances for major life events like marriage, children, education, home purchase, and retirement.
Calculate future costs adjusted for inflation, suggest SIP amounts, and create comprehensive life plans.
Be encouraging and help users achieve their life goals step by step.
Always include SEBI disclaimer when giving financial advice.""",

    "coupleplanner": """You are CoupleSathi, the Couple Money Planner.
You help couples plan joint finances, split expenses proportionally, and achieve shared goals together.
Explain the 50/30/20 budget rule, plan debt payoff strategies, and suggest fair contribution splits.
Be supportive of both partners and help build financial harmony in relationships.
Always include SEBI disclaimer when giving financial advice.""",
}


def call_openai(prompt: str, user_message: str, context: Optional[str] = None) -> str:
    """Call OpenAI API for AI response"""
    if not OPENAI_API_KEY:
        return "AI is not configured. Please set OPENAI_API_KEY environment variable."
    
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    messages = [
        {"role": "system", "content": prompt},
    ]
    
    if context:
        messages.append({"role": "system", "content": f"Context: {context}"})
    
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
        return f"Sorry, I encountered an error: {str(e)}"


def call_backend_api(endpoint: str, data: Dict[str, Any]) -> Optional[Dict]:
    """Call the FastAPI backend for calculations"""
    try:
        response = requests.post(
            f"http://localhost:8000{endpoint}",
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Backend API error: {e}")
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, agent: str):
    """Handle incoming message with AI response"""
    user_message = update.message.text
    prompt = AGENT_PROMPTS.get(agent, AGENT_PROMPTS["dhansarthi"])
    
    # Get AI response
    response = call_openai(prompt, user_message)
    
    await update.message.reply_text(response)


def create_bot(token: str, agent: str):
    """Create a Telegram bot for a specific agent"""
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", lambda u, c: handle_start(u, c, agent)))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda u, c: handle_message(u, c, agent)))
    
    return app


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE, agent: str):
    """Handle /start command"""
    agent_names = {
        "dhansarthi": "DhanSarthi",
        "karvid": "KarVid - Tax Wizard",
        "niveshak": "Niveshak - MF Analyst",
        "yojana": "YojanaKarta - FIRE Planner",
        "bazaar": "BazaarGuru - Market Research",
        "dhan": "DhanRaksha - Health Expert",
        "vidhi": "Vidhi - Compliance",
        "lifeevent": "JeevanSarthi - Life Event Advisor",
        "coupleplanner": "CoupleSathi - Couple Planner",
    }
    
    name = agent_names.get(agent, "AI Money Mentor")
    welcome_text = (
        f"Welcome to {name}!\n\n"
        f"I am your AI financial assistant. Ask me anything about:\n"
        f"- Tax planning\n- Mutual funds\n- FIRE planning\n- Stock prices\n- Financial health\n\n"
        f"How can I help you today?"
    )
    await update.message.reply_text(welcome_text)


if __name__ == "__main__":
    import sys
    agent = sys.argv[1] if len(sys.argv) > 1 else "dhansarthi"
    token = BOT_TOKENS.get(agent)
    
    if not token:
        print(f"Error: No token for agent {agent}. Set {agent.upper()}_BOT_TOKEN environment variable.")
        sys.exit(1)
    
    print(f"Starting {agent} bot...")
    app = create_bot(token, agent)
    app.run_polling()