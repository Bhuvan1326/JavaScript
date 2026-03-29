"""
Life Event Financial Advisor Agent
Helps users plan finances for major life events like marriage, children, education, retirement
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json

@dataclass
class LifeEvent:
    name: str
    estimated_cost: float
    years_until: int
    inflation_rate: float = 0.06  # 6% default inflation
    category: str = "general"

class LifeEventAdvisor:
    """Financial advisor for major life events"""
    
    # Average costs in India (in INR)
    EVENT_COSTS = {
        "marriage": {
            "min": 500000,
            "max": 5000000,
            "avg": 1500000,
            "description": "Wedding expenses including venue, catering, decorations"
        },
        "child_birth": {
            "min": 100000,
            "max": 500000,
            "avg": 200000,
            "description": "Hospital, prenatal care, initial setup"
        },
        "child_education": {
            "min": 500000,
            "max": 50000000,
            "avg": 10000000,
            "description": "Education from primary to higher education"
        },
        "home_purchase": {
            "min": 2000000,
            "max": 20000000,
            "avg": 8000000,
            "description": "Down payment for home purchase"
        },
        "car_purchase": {
            "min": 300000,
            "max": 3000000,
            "avg": 1000000,
            "description": "Vehicle purchase"
        },
        "higher_education": {
            "min": 500000,
            "max": 5000000,
            "avg": 1500000,
            "description": "MBA, MS, PhD abroad or in India"
        },
        "retirement": {
            "min": 10000000,
            "max": 100000000,
            "avg": 30000000,
            "description": "Retirement corpus target"
        },
        "emergency_fund": {
            "min": 100000,
            "max": 1000000,
            "avg": 300000,
            "description": "6-12 months expenses emergency fund"
        },
        "vacation": {
            "min": 50000,
            "max": 500000,
            "avg": 150000,
            "description": "Domestic or international vacation"
        },
        "parent_care": {
            "min": 500000,
            "max": 5000000,
            "avg": 1500000,
            "description": "Medical and care expenses for parents"
        }
    }
    
    def __init__(self):
        self.events: List[LifeEvent] = []
    
    def get_event_types(self) -> Dict[str, Dict]:
        """Return all available event types with costs"""
        return self.EVENT_COSTS
    
    def calculate_future_cost(
        self, 
        current_cost: float, 
        years: int, 
        inflation_rate: float = 0.06
    ) -> float:
        """Calculate future cost adjusted for inflation"""
        return current_cost * ((1 + inflation_rate) ** years)
    
    def calculate_monthly_sip(
        self,
        future_cost: float,
        years: int,
        expected_return: float = 0.12  # 12% equity returns
    ) -> float:
        """Calculate monthly SIP needed to reach goal"""
        if years <= 0:
            return future_cost
        
        monthly_rate = expected_return / 12
        months = years * 12
        
        # PMT formula for SIP
        if monthly_rate == 0:
            return future_cost / months
        
        sip = future_cost * monthly_rate / ((1 + monthly_rate) ** months - 1)
        return sip
    
    def calculate_lumpsum_needed(
        self,
        future_cost: float,
        years: int,
        expected_return: float = 0.12
    ) -> float:
        """Calculate lumpsum needed today to reach goal"""
        return future_cost / ((1 + expected_return) ** years)
    
    def plan_event(
        self,
        event_type: str,
        years_until: int,
        current_corpus: float = 0,
        monthly_investment: float = 0,
        inflation_rate: float = 0.06,
        expected_return: float = 0.12
    ) -> Dict[str, Any]:
        """Create comprehensive plan for a life event"""
        
        if event_type not in self.EVENT_COSTS:
            return {"error": f"Unknown event type: {event_type}"}
        
        event_info = self.EVENT_COSTS[event_type]
        current_cost = event_info["avg"]
        
        # Calculate future cost with inflation
        future_cost = self.calculate_future_cost(
            current_cost, years_until, inflation_rate
        )
        
        # Calculate SIP needed
        sip_needed = self.calculate_monthly_sip(
            future_cost - current_corpus, years_until, expected_return
        )
        
        # Calculate lumpsum needed
        lumpsum_needed = self.calculate_lumpsum_needed(
            future_cost, years_until, expected_return
        )
        
        # Calculate corpus from current monthly investment
        if monthly_investment > 0:
            future_corpus_from_sip = monthly_investment * (
                ((1 + expected_return/12) ** (years_until * 12) - 1) / (expected_return/12)
            )
        else:
            future_corpus_from_sip = 0
        
        # Calculate shortfall
        total_future_corpus = current_corpus * ((1 + expected_return) ** years_until) + future_corpus_from_sip
        shortfall = max(0, future_cost - total_future_corpus)
        
        return {
            "event": event_type,
            "description": event_info["description"],
            "current_cost": current_cost,
            "future_cost": round(future_cost, 2),
            "years_until": years_until,
            "inflation_adjusted_cost": round(future_cost, 2),
            "current_corpus": current_corpus,
            "monthly_investment": monthly_investment,
            "sip_needed": round(sip_needed, 2),
            "lumpsum_needed_today": round(lumpsum_needed, 2),
            "projected_corpus": round(total_future_corpus, 2),
            "shortfall": round(shortfall, 2),
            "is_achievable": shortfall <= 0,
            "recommendations": self._generate_recommendations(
                shortfall, years_until, event_type
            )
        }
    
    def _generate_recommendations(
        self, 
        shortfall: float, 
        years: int, 
        event_type: str
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if shortfall > 0:
            if years >= 5:
                recommendations.append("Consider equity mutual funds for higher returns over long term")
                recommendations.append("Start SIP in index funds for diversified exposure")
            elif years >= 3:
                recommendations.append("Hybrid funds (equity + debt) for balanced risk")
            else:
                recommendations.append("Focus on debt funds or FD for capital protection")
                recommendations.append("Consider reducing goal amount or extending timeline")
            
            recommendations.append(f"Increase monthly investment by ₹{round(shortfall / (years * 12), 0)}")
        else:
            recommendations.append("You're on track! Continue your current investment plan")
        
        # Event-specific recommendations
        if event_type == "marriage":
            recommendations.append("Consider pre-wedding expenses separately")
            recommendations.append("Book venues early for better deals")
        elif event_type == "child_education":
            recommendations.append("Explore education loan options for higher studies")
            recommendations.append("Consider 529 equivalent savings plans")
        elif event_type == "retirement":
            recommendations.append("Maximize PPF and NPS contributions")
            recommendations.append("Consider annuity plans for guaranteed income")
        
        return recommendations
    
    def comprehensive_life_plan(
        self,
        age: int,
        income: float,
        current_corpus: float = 0,
        events: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Create comprehensive financial plan for all life events"""
        
        # Default events based on age
        if events is None:
            events = self._get_default_events(age)
        
        plans = []
        total_monthly_sip = 0
        
        for event in events:
            plan = self.plan_event(
                event_type=event["type"],
                years_until=event["years"],
                current_corpus=event.get("current_corpus", 0),
                inflation_rate=event.get("inflation", 0.06),
                expected_return=event.get("return", 0.12)
            )
            plans.append(plan)
            total_monthly_sip += plan.get("sip_needed", 0)
        
        # Calculate affordability
        monthly_savings_capacity = income * 0.3  # 30% of income for savings
        affordable = total_monthly_sip <= monthly_savings_capacity
        
        return {
            "age": age,
            "income": income,
            "current_corpus": current_corpus,
            "monthly_savings_capacity": round(monthly_savings_capacity, 2),
            "total_monthly_sip_needed": round(total_monthly_sip, 2),
            "is_affordable": affordable,
            "events_planned": len(events),
            "plans": plans,
            "summary": {
                "total_future_cost": sum(p["future_cost"] for p in plans),
                "total_sip": round(total_monthly_sip, 2),
                "priority_order": sorted(
                    [p["event"] for p in plans], 
                    key=lambda x: next((e["years"] for e in events if e["type"] == x), 10)
                )
            }
        }
    
    def _get_default_events(self, age: int) -> List[Dict]:
        """Get default events based on age"""
        events = []
        
        if age < 25:
            events = [
                {"type": "higher_education", "years": 2},
                {"type": "car_purchase", "years": 5},
                {"type": "marriage", "years": 8},
                {"type": "emergency_fund", "years": 1}
            ]
        elif age < 30:
            events = [
                {"type": "marriage", "years": 3},
                {"type": "home_purchase", "years": 7},
                {"type": "child_birth", "years": 4},
                {"type": "emergency_fund", "years": 1}
            ]
        elif age < 40:
            events = [
                {"type": "child_education", "years": 5},
                {"type": "home_purchase", "years": 3},
                {"type": "parent_care", "years": 10},
                {"type": "retirement", "years": 25 - age + 40}
            ]
        elif age < 50:
            events = [
                {"type": "child_education", "years": 5},
                {"type": "parent_care", "years": 5},
                {"type": "retirement", "years": 60 - age}
            ]
        else:
            events = [
                {"type": "retirement", "years": max(60 - age, 1)},
                {"type": "parent_care", "years": 5}
            ]
        
        return events


# Convenience functions for API
def get_event_types():
    advisor = LifeEventAdvisor()
    return advisor.get_event_types()

def plan_life_event(
    event_type: str,
    years_until: int,
    current_corpus: float = 0,
    monthly_investment: float = 0,
    inflation_rate: float = 0.06,
    expected_return: float = 0.12
):
    advisor = LifeEventAdvisor()
    return advisor.plan_event(
        event_type, years_until, current_corpus, 
        monthly_investment, inflation_rate, expected_return
    )

def comprehensive_plan(
    age: int,
    income: float,
    current_corpus: float = 0,
    events: Optional[List[Dict]] = None
):
    advisor = LifeEventAdvisor()
    return advisor.comprehensive_life_plan(age, income, current_corpus, events)