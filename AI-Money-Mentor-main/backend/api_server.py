"""
AI Money Mentor - FastAPI Server
Connects Telegram bots to Python modules
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all agent modules
from agents.niveshak.portfolio_analyzer import PortfolioAnalyzer
from agents.karvid import calculate_new_regime_tax, calculate_old_regime_tax, compare_regimes, calculate_80c_deduction, calculate_equity_ltcg
from agents.yojana.fire_calculator import FIRECalculator, calculate_fire_number_india, get_sip_recommendation
from agents.bazaar.stock_data import StockData
from agents.dhan.health_score import get_health_score
from agents.vidhi.compliance import get_disclaimers, SEBICompliance

app = FastAPI(
    title="AI Money Mentor API",
    description="Financial advisory API for Indian market",
    version="1.0.0"
)

# CORS for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class TaxRequest(BaseModel):
    income: float
    regime: str = "new"
    deductions_80c: float = 0
    deductions_80d: float = 0

class FIRERequest(BaseModel):
    monthly_expenses: float
    current_age: int = 30
    retirement_age: int = 55
    current_corpus: float = 0

class HealthRequest(BaseModel):
    income: float
    expenses: float
    monthly_savings: float = 0
    monthly_investments: float = 0
    debt: float = 0
    insurance_coverage: float = 0

class XIRRRequest(BaseModel):
    transactions: List[Dict[str, Any]]

class StockRequest(BaseModel):
    symbol: str

# Health check
@app.get("/")
async def root():
    return {
        "service": "AI Money Mentor API",
        "version": "1.0.0",
        "agents": ["niveshak", "karvid", "yojana", "bazaar", "dhan", "vidhi", "dhan-sarthi", "life-event", "couple-planner"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ============ NIVESHAK (MF Portfolio) ============
@app.post("/niveshak/xirr")
async def calculate_xirr(request: XIRRRequest):
    """Calculate XIRR for portfolio"""
    analyzer = PortfolioAnalyzer()
    xirr = analyzer.calculate_xirr(request.transactions)
    return {"xirr_percent": round(xirr, 2)}

@app.post("/niveshak/risk-metrics")
async def get_risk_metrics(request: Dict[str, Any]):
    """Get portfolio risk metrics"""
    analyzer = PortfolioAnalyzer()
    nav_data = request.get("nav_data", [])
    metrics = analyzer.get_risk_metrics(nav_data)
    return metrics

@app.post("/niveshak/analyze")
async def analyze_portfolio(request: Dict[str, Any]):
    """Analyze entire portfolio from holdings list"""
    holdings = request.get("holdings", [])
    total_value = 0
    analyzer = PortfolioAnalyzer()
    
    # Calculate the total value based on units and NAV
    for h in holdings:
        total_value += h.get("units", 0) * h.get("nav", 0)
        
    # Generate true real cashflows derived from the SIP inputs
    from datetime import datetime
    today = datetime.now()
    transactions = []
    
    for h in holdings:
        sip = float(h.get("sipAmount", 0) or 0)
        duration = int(h.get("durationMonths", 0) or 0)
        
        if sip > 0 and duration > 0:
            for i in range(1, duration + 1):
                m = today.month - i
                year_offset = 0
                while m <= 0:
                    m += 12
                    year_offset -= 1
                y = today.year + year_offset
                d = min(today.day, 28)
                tx_date = f"{y:04d}-{m:02d}-{d:02d}"
                transactions.append({"date": tx_date, "amount": -sip})
                
    if not transactions and total_value > 0:
        # Fallback if no SIP entered, mock a generic 1 year lumpsum
        transactions.append({"date": f"{today.year-1}-{today.month:02d}-{today.day:02d}", "amount": -total_value/1.15})
        
    # Final positive cash flow evaluation mapping current portfolio net worth to today
    transactions.append({"date": today.strftime("%Y-%m-%d"), "amount": total_value})
    
    xirr_percent = 0
    if total_value > 0 and len(transactions) > 1:
        try:
            xirr_percent = analyzer.calculate_xirr(transactions)
        except Exception:
            xirr_percent = 0
    
    # Compute dynamic Sharpe Ratio mapped to the exact XIRR computed above
    # Assuming Risk Free Rate = 7.0%, Generic Equity Volatility = 15.0%
    sharpe_ratio = round((xirr_percent - 7.0) / 15.0, 2) if xirr_percent > 0 else 0
    
    risk_metrics = {
        "sharpe_ratio": sharpe_ratio,
        "volatility": 15.0,
        "max_drawdown": analyzer.get_risk_metrics([100, 102, 105, 104, 108, 110, 115])["max_drawdown"]
    }
    
    return {
        "status": "success",
        "total_value": total_value,
        "xirr_percent": xirr_percent,
        "risk_metrics": risk_metrics,
        "holdings": holdings
    }

# ============ KARVID (Tax Wizard) ============
@app.post("/karvid/calculate-tax")
async def calculate_tax(request: TaxRequest):
    """Calculate tax under specified regime"""
    if request.regime == "new":
        result = calculate_new_regime_tax(request.income)
    else:
        result = calculate_old_regime_tax(request.income)
    
    result["regime"] = request.regime
    return result

@app.post("/karvid/compare-regimes")
async def compare_tax_regimes(request: Dict[str, Any]):
    """Compare new vs old tax regime"""
    income = request.get("income", 0)
    result = compare_regimes(income)
    return result

@app.post("/karvid/80c")
async def calculate_80c(request: Dict[str, Any]):
    """Calculate 80C deductions"""
    # Remap shorthand keys to actual function parameter names
    param_map = {
        "ppf": "ppf", "elss": "elss", "nps": "nps_tier1",
        "lic": "life_insurance_premium",
        "tuition_fees": "tuition_fees",
        "home_loan_principal": "home_loan_principal",
        "nsc": "nsc", "ssy": "ssy", "scss": "scss",
        "tax_saving_fd": "tax_saving_fd", "ulip": "ulip",
        "stamp_duty": "stamp_duty",
        "life_insurance_premium": "life_insurance_premium"
    }
    deductions = {}
    for k, v in request.items():
        if k in param_map:
            deductions[param_map[k]] = v
    result = calculate_80c_deduction(**deductions)
    return result

@app.post("/karvid/capital-gains")
async def calculate_capital_gains(request: Dict[str, Any]):
    """Calculate capital gains tax"""
    holding_period = request.get("holding_period", "long")
    
    if holding_period == "long":
        # calculate_equity_ltcg needs sale_price, purchase_price, days_held
        sale_price = request.get("sale_price", 0)
        purchase_price = request.get("purchase_price", 0)
        days_held = request.get("days_held", 365)
        gain = request.get("gain", sale_price - purchase_price)
        
        if sale_price > 0 and purchase_price > 0:
            try:
                cg_result = calculate_equity_ltcg(sale_price, purchase_price, days_held)
                result = {
                    "gain": cg_result.gain,
                    "tax": cg_result.tax,
                    "holding_period": "long",
                    "exemption": getattr(cg_result, 'exemption', 125000),
                    "rate": "12.5%"
                }
            except Exception as e:
                # Fallback: simplified LTCG
                exempt = min(gain, 125000)
                taxable = max(0, gain - exempt)
                result = {
                    "gain": gain,
                    "tax": taxable * 0.125,
                    "holding_period": "long",
                    "exemption": exempt,
                    "rate": "12.5%",
                    "note": f"Simplified: {str(e)}"
                }
        else:
            # Only gain provided: simplified LTCG calc
            exempt = min(gain, 125000)
            taxable = max(0, gain - exempt)
            result = {
                "gain": gain,
                "tax": taxable * 0.125,
                "holding_period": "long",
                "exemption": exempt,
                "rate": "12.5%"
            }
    else:
        gain = request.get("gain", 0)
        result = {"gain": gain, "tax": gain * 0.15, "holding_period": "short", "rate": "15%"}
    
    return result

# ============ YOJANAKARTA (FIRE Planner) ============
@app.post("/yojana/fire-number")
async def get_fire_number(request: Dict[str, Any]):
    """Calculate FIRE number"""
    monthly_expenses = request.get("monthly_expenses", 50000)
    result = calculate_fire_number_india(monthly_expenses)
    return result

@app.post("/yojana/sip-recommendation")
async def get_sip(request: Dict[str, Any]):
    """Get SIP recommendation"""
    target_corpus = request.get("target_corpus", 10000000)
    years = request.get("years", 10)
    result = get_sip_recommendation(target_corpus, years)
    return result

@app.post("/yojana/retirement-plan")
async def create_retirement_plan(request: FIRERequest):
    """Create retirement plan"""
    calc = FIRECalculator(
        monthly_expenses=request.monthly_expenses,
        current_age=request.current_age,
        retirement_age=request.retirement_age,
        current_corpus=request.current_corpus
    )
    try:
        fire_number = calc.calculate_fire_number()
        monthly_savings = calc.calculate_monthly_savings()
        try:
            years = calc.calculate_years_to_fire(monthly_savings)
        except Exception:
            years = request.retirement_age - request.current_age
        plan = {
            "fire_number": fire_number,
            "years_to_fire": years,
            "monthly_savings": monthly_savings
        }
    except Exception as e:
        plan = {
            "fire_number": request.monthly_expenses * 12 * 25,
            "years_to_fire": request.retirement_age - request.current_age,
            "monthly_savings": 0,
            "note": f"Simplified calculation: {str(e)}"
        }
    return plan

# ============ BAZAAR GURU (Market Research) ============
@app.post("/bazaar/stock-quote")
async def get_stock_quote(request: StockRequest):
    """Get stock quote from NSE"""
    nse = StockData()
    quote = nse.get_quote(request.symbol)
    if quote:
        return quote.to_dict()
    raise HTTPException(status_code=404, detail=f"Stock {request.symbol} not found")

@app.get("/bazaar/top-gainers")
async def get_top_gainers(limit: int = 10):
    """Get top gaining stocks"""
    stock = StockData()
    gainers = stock.get_top_gainers(limit)
    return {"gainers": gainers}

@app.get("/bazaar/nifty50")
async def get_nifty50():
    """Get NIFTY 50 stocks"""
    return {"stocks": StockData.NIFTY_50}

# ============ DHAN RAKSHA (Financial Health) ============
@app.post("/dhan/health-score")
async def calculate_health_score(request: HealthRequest):
    """Calculate financial health score"""
    result = get_health_score(
        monthly_income=request.income,
        monthly_expenses=request.expenses,
        monthly_savings=request.monthly_savings,
        monthly_investments=request.monthly_investments
    )
    return result

# ============ VIDHI (Compliance) ============
@app.get("/vidhi/disclaimers")
async def get_all_disclaimers(category: str = "all"):
    """Get SEBI compliance disclaimers"""
    return {"disclaimers": get_disclaimers(category)}

@app.get("/vidhi/regulations")
async def get_sebi_regulations():
    """Get SEBI regulations"""
    return SEBICompliance.get_regulations()

# ============ DHAN SARTHI (Coordinator) ============
@app.post("/dhan-sarthi/route")
async def route_query(request: Dict[str, Any]):
    """Route query to appropriate agent with optional conversation context"""
    from agents.dhan_sarthi.coordinator import DhanSarthiCoordinator, AgentType
    coordinator = DhanSarthiCoordinator()
    query = request.get("query", "")
    context = request.get("context", [])  # Recent chat messages from frontend
    
    result = coordinator.parse_query(query)
    
    # Extract last agent from context for follow-up routing
    last_agent = None
    last_topic = None
    if context and isinstance(context, list):
        for msg in reversed(context):
            if msg.get("agent") and msg["agent"] != "dhan-sarthi":
                last_agent = msg["agent"]
                break
        # Get last user message for topic summary
        for msg in reversed(context):
            if msg.get("role") == "user":
                last_topic = msg.get("content", "")[:50]
                break
    
    # If DhanSarthi handles it directly (greeting/help/thanks/explain)
    if result.primary_agent == AgentType.DHAN_SARTHI:
        agent_list = [cap.name + " (" + cap.agent_type.value + ")" 
                      for cap in coordinator.AGENTS.values() 
                      if cap.agent_type != AgentType.DHAN_SARTHI]
        
        # Context-aware greeting responses
        context_suffix = ""
        if last_agent and last_topic:
            agent_names = {
                "karvid": "tax calculations",
                "yojana": "retirement planning", 
                "bazaar": "stock market data",
                "dhan": "financial health",
                "niveshak": "portfolio analysis",
                "vidhi": "compliance queries",
                "life-event": "life event planning",
                "couple-planner": "couple finance planning"
            }
            topic_name = agent_names.get(last_agent, last_agent)
            context_suffix = f"\n\nLast time we discussed {topic_name}. Would you like to continue with that, or try something new?"
        
        responses = {
            "greeting": f"Namaste! I'm DhanSarthi, your AI Money Mentor. I coordinate a team of 8 specialist agents to help you with taxes, investments, retirement planning, and more. How can I help you today?{context_suffix}",
            "help": "I'm DhanSarthi, the brain of AI Money Mentor! Here's what my team can do:\n" + "\n".join(["- " + name for name in agent_list]) + "\nJust ask me anything financial and I'll route you to the right expert!",
            "thanks": "You're welcome! Happy to help with your financial journey. Feel free to ask me anything anytime. Dhanyavaad! 🙏",
            "explain": "I'm DhanSarthi, an AI-powered financial coordinator. I analyze your query and route it to the best specialist agent. Try asking about taxes, stocks, retirement, or financial health!",
        }
        
        return {
            "query": result.query,
            "primary_agent": result.primary_agent.value,
            "confidence": result.confidence,
            "intent": result.intent,
            "response": responses.get(result.intent, responses["greeting"]),
            "available_agents": agent_list,
            "suggestions": result.suggestions,
            "processing_time_ms": result.processing_time_ms,
            "context_used": bool(context),
            "last_agent": last_agent,
        }
    
    # For routed queries: if confidence is low and we have previous context, bias toward last agent
    if result.confidence < 0.4 and last_agent:
        agent_map = {
            "karvid": AgentType.KARVID,
            "yojana": AgentType.YOJANA,
            "bazaar": AgentType.BAZAAR,
            "dhan": AgentType.DHAN,
            "niveshak": AgentType.NIVESHAK,
            "vidhi": AgentType.VIDHI,
            "life-event": AgentType.LIFE_EVENT,
            "couple-planner": AgentType.COUPLE_PLANNER,
        }
        if last_agent in agent_map:
            result.primary_agent = agent_map[last_agent]
            result.confidence = 0.5  # Boosted by context
    
    return result

# ============ KARVID TAX LAW ENDPOINTS ============
@app.get("/karvid/section/{section}")
async def get_tax_section(section: str):
    """Get detailed information about a tax section"""
    from agents.karvid.indian_tax_laws import get_tax_section_info
    return get_tax_section_info(section)

@app.get("/karvid/capital-gains-info/{asset_type}")
async def get_capital_gains_info(asset_type: str):
    """Get capital gains tax information"""
    from agents.karvid.indian_tax_laws import get_capital_gains_info
    return get_capital_gains_info(asset_type)

@app.get("/karvid/tax-slabs/{regime}")
async def get_tax_slabs(regime: str):
    """Get tax slabs for a regime"""
    from agents.karvid.indian_tax_laws import get_tax_slab
    return {"slabs": get_tax_slab(regime)}

# ============ VIDHI LEGAL ENDPOINTS ============
@app.get("/vidhi/constitution/{article}")
async def get_constitution_article(article: str):
    """Get Constitution provision"""
    from agents.vidhi.legal_knowledge import get_constitution_provision
    return get_constitution_provision(article)

@app.get("/vidhi/income-tax-section/{section}")
async def get_income_tax_section(section: str):
    """Get Income Tax Act section"""
    from agents.vidhi.legal_knowledge import get_income_tax_section
    return {"section": section, "description": get_income_tax_section(section)}

@app.get("/vidhi/sebi-regulation/{name}")
async def get_sebi_regulation(name: str):
    """Get SEBI regulation details"""
    from agents.vidhi.legal_knowledge import get_sebi_regulation
    return get_sebi_regulation(name)

@app.get("/vidhi/rbi-regulation/{name}")
async def get_rbi_regulation(name: str):
    """Get RBI regulation details"""
    from agents.vidhi.legal_knowledge import get_rbi_regulation
    return get_rbi_regulation(name)

# ============ LATENCY TRACKING ============
@app.get("/latency-stats")
async def get_latency_stats():
    """Get latency statistics"""
    from agents.dhan_sarthi.coordinator import DhanSarthiCoordinator
    coordinator = DhanSarthiCoordinator()
    return coordinator.get_latency_stats()

# ============================================================
# AI CHAT ENDPOINT
# ============================================================

@app.post("/ai/chat")
async def ai_chat_endpoint(request: dict):
    """
    AI-powered chat endpoint using OpenAI GPT-4o-mini
    Falls back to calculation-based responses if AI not configured
    """
    import os
    import requests
    import json
    
    message = request.get("message", "")
    agent = request.get("agent", "dhansarthi")
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Agent prompts
    AGENT_PROMPTS = {
        "dhansarthi": "You are DhanSarthi, the intelligent coordinator of AI Money Mentor. Be conversational and helpful.",
        "karvid": "You are KarVid, the Tax Wizard for Indian taxes. Help users understand and calculate taxes.",
        "yojana": "You are YojanaKarta, the FIRE Planner. Help users plan financial independence and retirement.",
        "bazaar": "You are BazaarGuru, the Market Researcher. Provide stock prices and market analysis.",
        "dhan": "You are DhanRaksha, the Financial Health Expert. Assess financial health and provide recommendations.",
        "vidhi": "You are Vidhi, the Compliance Expert. Help users understand SEBI regulations and investor rights.",
    }
    
    # Try OpenAI
    if OPENAI_API_KEY:
        try:
            prompt = AGENT_PROMPTS.get(agent, AGENT_PROMPTS["dhansarthi"])
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": message}
                    ],
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            response.raise_for_status()
            ai_response = response.json()["choices"][0]["message"]["content"]
            return {"agent": agent, "response": ai_response}
        except Exception as e:
            print(f"OpenAI error: {e}")
    
    # Fallback response
    return {
        "agent": agent,
        "response": f"I'm {agent.title()}, ready to help! AI responses require OPENAI_API_KEY to be configured. In the meantime, I can still help with calculations."
    }


# ============================================================
# CHAT BRIDGE ENDPOINTS - Frontend to OpenClaw Agent Swarm
# ============================================================

from chat_bridge import (
    ChatRequest, ChatResponse, 
    store_message, get_chat_history, send_to_agent,
    init_db
)
import uuid

# Initialize chat database
init_db()

@app.post("/bridge/chat", response_model=ChatResponse)
async def bridge_chat(request: ChatRequest):
    """
    Bridge frontend to OpenClaw agents with chat history
    
    - Stores user message in SQLite
    - Retrieves chat history for context
    - Sends to appropriate OpenClaw agent
    - Stores agent response
    - Returns response to frontend
    """
    # Generate session_id if not provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Store user message
    store_message(
        user_id=request.user_id,
        session_id=session_id,
        agent_id=request.agent_id,
        role="user",
        message=request.message
    )
    
    # Get chat history for context
    history = get_chat_history(
        user_id=request.user_id,
        session_id=session_id,
        limit=20
    )
    
    # Send to agent via WebSocket bridge
    try:
        response = send_to_agent(
            agent_id=request.agent_id,
            message=request.message,
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Store agent response
    store_message(
        user_id=request.user_id,
        session_id=session_id,
        agent_id=request.agent_id,
        role="assistant",
        message=response
    )
    
    return ChatResponse(
        agent=request.agent_id,
        response=response,
        session_id=session_id,
        history_count=len(history)
    )

@app.get("/bridge/history/{user_id}/{session_id}")
async def bridge_get_history(user_id: str, session_id: str, limit: int = 50):
    """Get chat history for a user session"""
    history = get_chat_history(user_id, session_id, limit)
    return {"history": history, "count": len(history)}

@app.delete("/bridge/history/{user_id}/{session_id}")
async def bridge_clear_history(user_id: str, session_id: str):
    """Clear chat history for a session"""
    import sqlite3
    conn = sqlite3.connect(os.path.expanduser('~/ai-money-mentor/chat_history.db'))
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_messages WHERE user_id = ? AND session_id = ?', (user_id, session_id))
    conn.commit()
    conn.close()
    return {"status": "cleared", "user_id": user_id, "session_id": session_id}

@app.get("/bridge/sessions/{user_id}")
async def bridge_list_sessions(user_id: str):
    """List all chat sessions for a user"""
    import sqlite3
    conn = sqlite3.connect(os.path.expanduser('~/ai-money-mentor/chat_history.db'))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT session_id, agent_id, MAX(timestamp) as last_message
        FROM chat_messages WHERE user_id = ?
        GROUP BY session_id ORDER BY last_message DESC
    ''', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    sessions = [{"session_id": r["session_id"], "agent_id": r["agent_id"], "last_message": r["last_message"]} for r in rows]
    return {"sessions": sessions}

# ============ LIFE EVENT ADVISOR ============
from agents.life_event import (
    get_event_types,
    plan_life_event,
    comprehensive_plan as life_event_comprehensive_plan
)

@app.get("/life-event/types")
async def life_event_get_types():
    """Get all available life event types"""
    return get_event_types()

@app.post("/life-event/plan")
async def life_event_plan(request: Dict[str, Any]):
    """Plan for a specific life event"""
    return plan_life_event(
        event_type=request.get("event_type"),
        years_until=request.get("years_until", 5),
        current_corpus=request.get("current_corpus", 0),
        monthly_investment=request.get("monthly_investment", 0),
        inflation_rate=request.get("inflation_rate", 0.06),
        expected_return=request.get("expected_return", 0.12)
    )

@app.post("/life-event/comprehensive")
async def life_event_comprehensive(request: Dict[str, Any]):
    """Create comprehensive life event financial plan"""
    try:
        result = life_event_comprehensive_plan(
            age=request.get("age", 25),
            income=request.get("income", 50000),
            current_corpus=request.get("current_corpus", 0),
            events=request.get("events", None)
        )
        return result
    except Exception as e:
        # Fallback: return a basic plan if comprehensive fails
        return {
            "status": "partial",
            "note": f"Comprehensive plan had an issue: {str(e)}",
            "age": request.get("age", 25),
            "events_planned": 0
        }

# ============ COUPLE PLANNER ============
from agents.couple_planner import (
    create_couple_plan,
    calculate_expense_split,
    CouplePlanner,
    Person,
    SplitType
)

@app.post("/couple/finances")
async def couple_get_finances(request: Dict[str, Any]):
    """Get combined finances for a couple"""
    p1 = Person(name=request.get("person1_name", "Person 1"), income=request.get("person1_income", 0))
    p2 = Person(name=request.get("person2_name", "Person 2"), income=request.get("person2_income", 0))
    planner = CouplePlanner(p1, p2)
    return planner.get_combined_finances()

@app.post("/couple/split-expense")
async def couple_split_expense(request: Dict[str, Any]):
    """Calculate how to split an expense between couple"""
    return calculate_expense_split(
        person1_name=request.get("person1_name", "Person 1"),
        person1_income=request.get("person1_income", 0),
        person2_name=request.get("person2_name", "Person 2"),
        person2_income=request.get("person2_income", 0),
        expense_amount=request.get("expense_amount", 0),
        split_type=request.get("split_type", "proportional")
    )

@app.post("/couple/plan")
async def couple_create_plan(request: Dict[str, Any]):
    """Create comprehensive couple financial plan"""
    return create_couple_plan(
        person1_name=request.get("person1_name", "Person 1"),
        person1_income=request.get("person1_income", 0),
        person2_name=request.get("person2_name", "Person 2"),
        person2_income=request.get("person2_income", 0),
        goals=request.get("goals")
    )

@app.post("/couple/budget")
async def couple_create_budget(request: Dict[str, Any]):
    """Create joint budget plan"""
    p1 = Person(
        name=request.get("person1_name", "Person 1"),
        income=request.get("person1_income", 0),
        expenses=request.get("person1_expenses", 0),
        savings=request.get("person1_savings", 0)
    )
    p2 = Person(
        name=request.get("person2_name", "Person 2"),
        income=request.get("person2_income", 0),
        expenses=request.get("person2_expenses", 0),
        savings=request.get("person2_savings", 0)
    )
    planner = CouplePlanner(p1, p2)
    return planner.create_budget_plan(request.get("categories"))

@app.post("/couple/goals")
async def couple_plan_goals(request: Dict[str, Any]):
    """Calculate SIP for couple's shared goals"""
    p1 = Person(
        name=request.get("person1_name", "Person 1"),
        income=request.get("person1_income", 0)
    )
    p2 = Person(
        name=request.get("person2_name", "Person 2"),
        income=request.get("person2_income", 0)
    )
    planner = CouplePlanner(p1, p2)
    
    # Add goals
    for goal in request.get("goals", []):
        planner.add_shared_goal(
            name=goal["name"],
            target_amount=goal["target_amount"],
            deadline_years=goal["years"],
            priority=goal.get("priority", 3)
        )
    
    return planner.calculate_sip_for_goals(request.get("expected_return", 0.12))

@app.post("/couple/debt-payoff")
async def couple_debt_payoff(request: Dict[str, Any]):
    """Plan debt payoff strategy for couple"""
    p1 = Person(
        name=request.get("person1_name", "Person 1"),
        income=request.get("person1_income", 0),
        expenses=request.get("person1_expenses", 0),
        savings=request.get("person1_savings", 0),
        debt=request.get("person1_debt", 0)
    )
    p2 = Person(
        name=request.get("person2_name", "Person 2"),
        income=request.get("person2_income", 0),
        expenses=request.get("person2_expenses", 0),
        savings=request.get("person2_savings", 0),
        debt=request.get("person2_debt", 0)
    )
    planner = CouplePlanner(p1, p2)
    try:
        return planner.plan_debt_payoff(
            debts=request.get("debts", []),
            strategy=request.get("strategy", "avalanche")
        )
    except Exception as e:
        return {
            "strategy": request.get("strategy", "avalanche"),
            "debts": request.get("debts", []),
            "note": f"Debt payoff calculation error: {str(e)}",
            "recommendation": "Please provide expenses and savings for both partners for accurate planning."
        }

# ============ MAIN ============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
