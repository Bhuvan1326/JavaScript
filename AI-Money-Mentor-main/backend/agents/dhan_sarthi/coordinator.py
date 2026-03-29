"""
DhanSarthi Coordinator - The Brain of AI Money Mentor
Routes queries to appropriate specialist agents with intelligence
"""

import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import requests


class AgentType(Enum):
    """Available specialist agents"""
    DHAN_SARTHI = "dhan-sarthi" # Coordinator/Greeting/Generic
    NIVESHAK = "niveshak"       # MF Portfolio X-Ray
    KARVID = "karvid"           # Tax Wizard
    YOJANAKARTA = "yojana"      # FIRE Planner
    BAZAAR_GURU = "bazaar"      # Market Research
    DHAN_RAKSHA = "dhan"        # Financial Health
    VIDHI = "vidhi"             # Legal/Compliance
    LIFE_EVENT = "life-event"   # Life Event Planner
    COUPLE_PLANNER = "couple-planner"  # Couple Finance


@dataclass
class AgentCapability:
    """Agent capability description"""
    name: str
    agent_type: AgentType
    description: str
    keywords: List[str]
    example_queries: List[str]
    confidence_threshold: float = 0.6
    can_delegate: bool = True
    api_endpoint: str = ""


@dataclass
class RoutingResult:
    """Result of query routing"""
    query: str
    primary_agent: AgentType
    confidence: float
    intent: str
    secondary_agents: List[AgentType]
    api_endpoint: str
    suggestions: List[str]
    processing_time_ms: float = 0


@dataclass
class QueryResult:
    """Result of executing a query"""
    query: str
    agent: str
    result: Any
    processing_time_ms: float
    api_endpoint: str
    from_cache: bool = False


class DhanSarthiCoordinator:
    """
    The Brain of AI Money Mentor
    
    Responsibilities:
    1. Parse user queries with intelligence
    2. Route to correct agent(s) with confidence
    3. Delegate tasks to multiple agents if needed
    4. Aggregate results intelligently
    5. Handle doubts and provide clarifications
    6. Track latency for optimization
    """
    
    API_BASE = "http://localhost:8000"
    
    # Agent capabilities with detailed knowledge
    AGENTS: Dict[AgentType, AgentCapability] = {
        AgentType.DHAN_SARTHI: AgentCapability(
            name="DhanSarthi",
            agent_type=AgentType.DHAN_SARTHI,
            description="AI Money Mentor Coordinator - Greets, explains capabilities, routes queries to specialist agents",
            keywords=["hello", "hi", "hey", "namaste", "namaskar", "good morning", "good evening",
                     "good afternoon", "help", "what can you do", "who are you", "about",
                     "explain", "how does it work", "what is this", "start", "menu",
                     "thank", "thanks", "dhanyavaad", "shukriya", "bye", "goodbye"],
            example_queries=[
                "Hello!",
                "What can you do?",
                "Who are you?",
                "How does this work?",
                "Thank you for the help!",
            ],
            confidence_threshold=0.3,
            can_delegate=False,
            api_endpoint="/dhan-sarthi/route"
        ),
        AgentType.NIVESHAK: AgentCapability(
            name="Niveshak",
            agent_type=AgentType.NIVESHAK,
            description="Mutual Fund Portfolio Analyst - CAS parsing, XIRR, Sharpe ratio, portfolio analysis, risk metrics",
            keywords=["mf", "mutual fund", "portfolio", "cas", "xirr", "nav", "sip", "cagr", "sharpe", 
                     "sortino", "holding", "scheme", "fund", "investment", "returns", "risk"],
            example_queries=[
                "Analyze my mutual fund portfolio",
                "Calculate XIRR for my investments",
                "What is my Sharpe ratio?",
                "Parse my CAS statement",
                "Which funds should I redeem?",
            ],
            confidence_threshold=0.6,
            api_endpoint="/niveshak/xirr"
        ),
        AgentType.KARVID: AgentCapability(
            name="KarVid",
            agent_type=AgentType.KARVID,
            description="Tax Wizard - Indian tax calculations, all sections of Income Tax Act, regime comparison, deductions, capital gains",
            keywords=["tax", "income tax", "80c", "80d", "80ccd", "regime", "deduction", "capital gains", 
                     "ltcg", "stcg", "itr", "form 16", "tds", "advance tax", "assessment", "penalty",
                     "new regime", "old regime", "rebate", "87a", "slab", "exemption", "sec", "section"],
            example_queries=[
                "Calculate my tax for 15 lakhs",
                "Which regime is better for me?",
                "How much can I save with 80C?",
                "What is capital gains tax on stocks?",
                "Section 80C deduction limit",
                "Explain Section 54 exemption",
                "Tax on LTCG from equity",
            ],
            confidence_threshold=0.5,
            api_endpoint="/karvid/calculate-tax"
        ),
        AgentType.YOJANAKARTA: AgentCapability(
            name="YojanaKarta",
            agent_type=AgentType.YOJANAKARTA,
            description="Financial Planner - FIRE planning, SIP roadmaps, goal-based investing, retirement planning",
            keywords=["fire", "retire", "sip", "goal", "corpus", "retirement", "financial independence", 
                     "roadmap", "plan", "savings", "invest monthly", "target", "years", "compound"],
            example_queries=[
                "What is my FIRE number?",
                "How much should I invest monthly?",
                "Plan my retirement",
                "When can I retire?",
                "SIP for 1 crore in 15 years",
            ],
            confidence_threshold=0.6,
            api_endpoint="/yojana/fire-number"
        ),
        AgentType.BAZAAR_GURU: AgentCapability(
            name="BazaarGuru",
            agent_type=AgentType.BAZAAR_GURU,
            description="Market Researcher - NSE/BSE stock data, stock screening, market analysis, company information",
            keywords=["stock", "nse", "bse", "market", "price", "quote", "screener", "nifty", "sensex", 
                     "equity", "share", "company", "ipo", "listing", "gainer", "loser", "volume",
                     "happiestminds", "reliance", "tcs", "infy", "hdfc", "icici"],
            example_queries=[
                "Get RELIANCE stock price",
                "Show top gainers today",
                "What is NIFTY?",
                "Screen stocks by P/E ratio",
                "HappiestMinds stock analysis",
                "Is this stock good or bad?",
            ],
            confidence_threshold=0.5,
            api_endpoint="/bazaar/stock-quote"
        ),
        AgentType.DHAN_RAKSHA: AgentCapability(
            name="DhanRaksha",
            agent_type=AgentType.DHAN_RAKSHA,
            description="Financial Health Expert - 8-factor assessment, emergency fund, debt-to-income, savings rate, insurance",
            keywords=["health", "score", "emergency", "debt", "savings", "insurance", "credit", "financial health",
                     "checkup", "assess", "emergency fund", "ratio", "coverage", "readiness"],
            example_queries=[
                "What is my financial health score?",
                "How healthy are my finances?",
                "Give me a financial checkup",
                "Am I saving enough?",
                "Do I have enough emergency fund?",
            ],
            confidence_threshold=0.6,
            api_endpoint="/dhan/health-score"
        ),
        AgentType.VIDHI: AgentCapability(
            name="Vidhi",
            agent_type=AgentType.VIDHI,
            description="Legal Advisor - SEBI regulations, Income Tax Act sections, Constitution provisions, RBI regulations, compliance",
            keywords=["sebi", "compliance", "legal", "disclaimer", "regulation", "advisor", "law", "act",
                     "constitution", "section", "rbi", "fema", "pmla", "court", "judgment", "rights",
                     "article", "income tax act", "section 80c", "section 54", "article 265"],
            example_queries=[
                "What SEBI regulations apply?",
                "Explain Section 80C of Income Tax Act",
                "What is Article 265?",
                "SEBI registration requirements",
                "RBI regulations for banks",
                "Consumer Protection Act",
            ],
            confidence_threshold=0.5,
            api_endpoint="/vidhi/disclaimers"
        ),
        AgentType.LIFE_EVENT: AgentCapability(
            name="Life Event Advisor",
            agent_type=AgentType.LIFE_EVENT,
            description="Life Event Planner - Marriage, child birth, education, home buying financial planning",
            keywords=["marriage", "wedding", "married", "baby", "child", "birth", "education", 
                     "college", "school", "home buy", "house", "property", "life event",
                     "marriage planning", "child birth", "higher education", "getting married",
                     "new born", "kid", "university", "abroad", "study"],
            example_queries=[
                "I am getting married next year",
                "Plan finances for having a baby",
                "How much to save for child's education?",
                "Planning to buy a house in 5 years",
            ],
            confidence_threshold=0.5,
            api_endpoint="/life-event/plan"
        ),
        AgentType.COUPLE_PLANNER: AgentCapability(
            name="Couple's Planner",
            agent_type=AgentType.COUPLE_PLANNER,
            description="Joint Finance Manager - Shared budgets, expense splitting, joint debt payoff, couple's financial planning",
            keywords=["couple", "wife", "husband", "spouse", "partner", "joint", "together",
                     "split", "shared", "both of us", "we", "our budget", "combined",
                     "joint budget", "dual income", "expense split", "joint finance",
                     "couple finance", "family budget", "partner income"],
            example_queries=[
                "Plan joint budget with my wife",
                "How should we split expenses?",
                "Combined debt payoff strategy",
                "Manage finances as a couple",
            ],
            confidence_threshold=0.5,
            api_endpoint="/couple/finances"
        ),
    }
    
    def __init__(self):
        """Initialize coordinator with latency tracking"""
        self.conversation_history: List[Dict] = []
        self.latency_stats: Dict[str, List[float]] = {
            "routing": [],
            "api_call": [],
            "total": [],
        }
    
    def parse_query(self, query: str) -> RoutingResult:
        """
        Parse user query with intelligent keyword matching
        
        Args:
            query: User's natural language query
            
        Returns:
            RoutingResult with agent, confidence, and timing
        """
        start_time = time.time()
        query_lower = query.lower().strip()
        
        # ---- GREETING / GENERIC DETECTION (before keyword scoring) ----
        greetings = ["hello", "hi", "hey", "namaste", "namaskar", "good morning",
                     "good evening", "good afternoon", "good night", "howdy",
                     "sup", "yo", "hola", "greetings"]
        help_words = ["what can you do", "who are you", "help me", "what is this",
                      "how does this work", "what do you do", "about", "menu",
                      "capabilities", "features", "start"]
        thanks_words = ["thank", "thanks", "dhanyavaad", "shukriya", "bye",
                        "goodbye", "see you", "take care"]
        explain_words = ["what is", "explain", "how does", "tell me about",
                         "meaning of", "define"]
        
        # Check for pure greetings (nothing else meaningful)
        is_greeting = any(query_lower.startswith(g) or query_lower == g for g in greetings)
        is_help = any(h in query_lower for h in help_words)
        is_thanks = any(t in query_lower for t in thanks_words)
        is_generic_explain = any(query_lower.startswith(e) for e in explain_words)
        
        # If it's a pure greeting/help/thanks with no finance-specific keywords
        finance_specifics = ["tax", "stock", "fund", "sip", "fire", "retire", "income",
                            "invest", "portfolio", "deduction", "regime", "nifty", "share",
                            "sebi", "health score", "capital gain", "marriage", "couple",
                            "wife", "husband", "baby", "wedding", "mutual fund"]
        has_finance_content = any(f in query_lower for f in finance_specifics)
        
        if (is_greeting or is_help or is_thanks) and not has_finance_content:
            processing_time = (time.time() - start_time) * 1000
            self.latency_stats["routing"].append(processing_time)
            
            intent = "greeting"
            if is_help: intent = "help"
            elif is_thanks: intent = "thanks"
            
            return RoutingResult(
                query=query,
                primary_agent=AgentType.DHAN_SARTHI,
                confidence=1.0,
                intent=intent,
                secondary_agents=[],
                api_endpoint="/dhan-sarthi/route",
                suggestions=[cap.example_queries[0] for cap in list(self.AGENTS.values())[1:5]],
                processing_time_ms=processing_time
            )
        
        # For generic explanations without finance keywords, handle via DhanSarthi
        if is_generic_explain and not has_finance_content:
            processing_time = (time.time() - start_time) * 1000
            self.latency_stats["routing"].append(processing_time)
            return RoutingResult(
                query=query,
                primary_agent=AgentType.DHAN_SARTHI,
                confidence=0.8,
                intent="explain",
                secondary_agents=[],
                api_endpoint="/dhan-sarthi/route",
                suggestions=[cap.example_queries[0] for cap in list(self.AGENTS.values())[1:5]],
                processing_time_ms=processing_time
            )
        
        # Score each agent based on keyword matches
        agent_scores: Dict[AgentType, float] = {}
        matched_keywords: Dict[AgentType, List[str]] = {}
        
        for agent_type, capability in self.AGENTS.items():
            score = 0.0
            matches = []
            
            # Keyword matching
            for keyword in capability.keywords:
                if keyword in query_lower:
                    score += 1.0
                    matches.append(keyword)
            
            # Bonus for exact phrase matches
            for keyword in capability.keywords:
                if f" {keyword} " in f" {query_lower} ":
                    score += 0.5
            
            # Extra bonus for section/article mentions (legal/tax queries)
            if agent_type == AgentType.KARVID:
                if "section" in query_lower or "sec" in query_lower:
                    score += 2.0
            if agent_type == AgentType.VIDHI:
                if "article" in query_lower or "act" in query_lower:
                    score += 2.0
            
            # Stock symbol matching
            if agent_type == AgentType.BAZAAR_GURU:
                for symbol in ["reliance", "tcs", "infosys", "hdfc", "icici", "happiestminds", "happstmnds"]:
                    if symbol in query_lower:
                        score += 2.0
            
            # Life event priority: marriage/baby/education get strong boost
            if agent_type == AgentType.LIFE_EVENT:
                for trigger in ["marriage", "wedding", "married", "baby", "child", "birth", "education", "college"]:
                    if trigger in query_lower:
                        score += 3.0  # Strong boost to override Yojana's generic "plan"
            
            # Couple planner priority: couple/wife/husband/joint get strong boost
            if agent_type == AgentType.COUPLE_PLANNER:
                for trigger in ["couple", "wife", "husband", "spouse", "partner", "joint", "both of us"]:
                    if trigger in query_lower:
                        score += 3.0  # Strong boost to override Yojana's generic "plan"
            
            agent_scores[agent_type] = score
            matched_keywords[agent_type] = matches
        
        # Normalize scores
        max_score = max(agent_scores.values()) if agent_scores else 1.0
        if max_score > 0:
            agent_scores = {k: v/max_score for k, v in agent_scores.items()}
        
        # Get primary agent (highest score)
        primary_agent = max(agent_scores.items(), key=lambda x: x[1]) if agent_scores else (AgentType.DHAN_RAKSHA, 0.0)
        
        # Get secondary agents (score > 0.3)
        secondary_agents = [a for a, s in agent_scores.items() if s > 0.3 and a != primary_agent[0]]
        
        # Determine intent
        intent = self._determine_intent(query_lower, primary_agent[0])
        
        processing_time = (time.time() - start_time) * 1000
        self.latency_stats["routing"].append(processing_time)
        
        return RoutingResult(
            query=query,
            primary_agent=primary_agent[0],
            confidence=primary_agent[1],
            intent=intent,
            secondary_agents=secondary_agents,
            api_endpoint=self.AGENTS[primary_agent[0]].api_endpoint,
            suggestions=self.AGENTS[primary_agent[0]].example_queries[:3],
            processing_time_ms=processing_time
        )
    
    def _determine_intent(self, query: str, agent: AgentType) -> str:
        """Determine the specific intent within an agent"""
        if agent == AgentType.NIVESHAK:
            if "xirr" in query: return "calculate_xirr"
            if "risk" in query: return "analyze_risk"
            if "holding" in query or "portfolio" in query: return "show_holdings"
            return "analyze_portfolio"
        
        elif agent == AgentType.KARVID:
            if "regime" in query or "which regime" in query: return "compare_regimes"
            if "80c" in query or "80d" in query: return "calculate_deductions"
            if "section" in query: return "explain_section"
            if "capital gain" in query or "ltcg" in query or "stcg" in query: return "calculate_capital_gains"
            return "calculate_tax"
        
        elif agent == AgentType.YOJANAKARTA:
            if "fire" in query: return "calculate_fire_number"
            if "sip" in query: return "plan_sip"
            if "retire" in query: return "plan_retirement"
            return "plan_finances"
        
        elif agent == AgentType.BAZAAR_GURU:
            if "price" in query or "quote" in query: return "get_stock_price"
            if "screen" in query: return "screen_stocks"
            if "good" in query or "bad" in query or "analysis" in query: return "analyze_stock"
            return "market_overview"
        
        elif agent == AgentType.DHAN_RAKSHA:
            return "calculate_health_score"
        
        elif agent == AgentType.VIDHI:
            if "section" in query: return "explain_section"
            if "sebi" in query: return "sebi_regulations"
            if "article" in query: return "constitution_article"
            return "get_disclaimers"
        
        elif agent == AgentType.LIFE_EVENT:
            if "type" in query: return "get_event_types"
            if any(w in query for w in ["comprehensive", "full", "detailed"]): return "comprehensive_plan"
            return "plan_life_event"
        
        elif agent == AgentType.COUPLE_PLANNER:
            if "split" in query: return "split_expense"
            if "budget" in query: return "couple_budget"
            if "debt" in query: return "couple_debt_payoff"
            return "couple_finances"
        
        return "general_query"
    
    def execute_query(self, query: str, params: Dict = None) -> QueryResult:
        """
        Execute a query by routing to the appropriate agent and calling the API
        
        Args:
            query: User's query
            params: Additional parameters for the API call
            
        Returns:
            QueryResult with data and timing
        """
        start_time = time.time()
        
        # Parse and route
        routing = self.parse_query(query)
        
        # Call API
        api_result = None
        try:
            endpoint = f"{self.API_BASE}{routing.api_endpoint}"
            api_start = time.time()
            
            if routing.intent in ["calculate_tax", "compare_regimes", "calculate_deductions"]:
                # POST with income param
                data = params or {}
                if "income" not in data:
                    # Try to extract income from query
                    import re
                    match = re.search(r'(\d+)\s*(lakh|lac|k)?', query.lower())
                    if match:
                        income = int(match.group(1))
                        if match.group(2) in ["lakh", "lac"]:
                            income *= 100000
                        data["income"] = income
                response = requests.post(endpoint, json=data, timeout=30)
            
            elif routing.intent in ["get_stock_price", "analyze_stock"]:
                # POST with symbol
                data = params or {}
                if "symbol" not in data:
                    # Try to extract symbol from query
                    symbols = {
                        "reliance": "RELIANCE", "tcs": "TCS", "infosys": "INFY",
                        "hdfc": "HDFCBANK", "icici": "ICICIBANK", "happiestminds": "HAPPSTMNDS",
                        "happstmnds": "HAPPSTMNDS"
                    }
                    for key, sym in symbols.items():
                        if key in query.lower():
                            data["symbol"] = sym
                            break
                response = requests.post(endpoint, json=data, timeout=30)
            
            elif routing.intent == "calculate_fire_number":
                # POST with monthly expenses - SMART EXTRACTION
                data = params or {}
                if "monthly_expenses" not in data:
                    import re
                    # Look for expenses pattern FIRST (before any income/tax numbers)
                    # Pattern 1: "expenses are Xk" or "monthly expenses X"
                    expenses_match = re.search(r'(?:expenses?|spend|spending)\s*(?:are|is)?\s*(\d+)\s*(k|thousand|lakh)?', query.lower())
                    if expenses_match:
                        expenses = int(expenses_match.group(1))
                        if expenses_match.group(2) == "k":
                            expenses *= 1000
                        elif expenses_match.group(2) == "lakh":
                            expenses *= 100000
                        data["monthly_expenses"] = expenses
                    else:
                        # Pattern 2: "Xk monthly" or "Xk expenses"
                        alt_match = re.search(r'(\d+)\s*(k|thousand)?\s*(?:monthly|expenses|per month)', query.lower())
                        if alt_match:
                            expenses = int(alt_match.group(1))
                            if alt_match.group(2) == "k":
                                expenses *= 1000
                            data["monthly_expenses"] = expenses
                response = requests.post(endpoint, params=data, timeout=30)
            
            else:
                # GET request
                response = requests.get(endpoint, timeout=30)
            
            api_time = (time.time() - api_start) * 1000
            self.latency_stats["api_call"].append(api_time)
            
            if response.status_code == 200:
                api_result = response.json()
            else:
                api_result = {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            api_result = {"error": str(e)}
        
        total_time = (time.time() - start_time) * 1000
        self.latency_stats["total"].append(total_time)
        
        return QueryResult(
            query=query,
            agent=routing.primary_agent.value,
            result=api_result,
            processing_time_ms=total_time,
            api_endpoint=routing.api_endpoint
        )
    
    def delegate_task(self, query: str, agents: List[AgentType]) -> Dict[AgentType, QueryResult]:
        """
        Delegate a task to multiple agents and aggregate results
        
        Args:
            query: User's query
            agents: List of agents to delegate to
            
        Returns:
            Dict mapping each agent to its QueryResult
        """
        results = {}
        for agent in agents:
            routing = self.parse_query(query)
            if routing.primary_agent == agent:
                results[agent] = self.execute_query(query)
        return results
    
    def handle_doubt(self, query: str, doubt: str) -> str:
        """
        Handle user's doubt or clarification request
        
        Args:
            query: Original query
            doubt: User's doubt or clarification question
            
        Returns:
            Clarification response
        """
        routing = self.parse_query(query)
        capability = self.AGENTS[routing.primary_agent]
        
        response = f"I understand your doubt about: '{doubt}'\n\n"
        response += f"You asked about {capability.name}'s capabilities.\n\n"
        response += f"{capability.description}\n\n"
        response += "Here are some example queries you can try:\n"
        for ex in capability.example_queries[:3]:
            response += f"• {ex}\n"
        
        return response
    
    def get_all_agents(self) -> List[Dict]:
        """Get list of all available agents"""
        return [
            {
                "name": cap.name,
                "type": cap.agent_type.value,
                "description": cap.description,
                "keywords": cap.keywords,
                "api_endpoint": cap.api_endpoint,
            }
            for cap in self.AGENTS.values()
        ]
    
    def get_latency_stats(self) -> Dict[str, Dict[str, float]]:
        """Get latency statistics"""
        stats = {}
        for key, values in self.latency_stats.items():
            if values:
                stats[key] = {
                    "min_ms": min(values),
                    "max_ms": max(values),
                    "avg_ms": sum(values) / len(values),
                    "count": len(values),
                }
        return stats


def create_coordinator() -> DhanSarthiCoordinator:
    """Factory function to create coordinator"""
    return DhanSarthiCoordinator()
