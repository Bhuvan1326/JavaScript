"""
Couple's Money Planner Agent
Helps couples plan joint finances, shared goals, and manage money together
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class SplitType(Enum):
    EQUAL = "equal"
    PROPORTIONAL = "proportional"  # Based on income ratio
    CUSTOM = "custom"

@dataclass
class Person:
    name: str
    income: float
    expenses: float = 0
    savings: float = 0
    debt: float = 0
    investments: float = 0

@dataclass
class SharedGoal:
    name: str
    target_amount: float
    deadline_years: int
    priority: int  # 1-5, 1 being highest
    contribution_split: Dict[str, float]  # person_name: percentage

class CouplePlanner:
    """Financial planner for couples"""
    
    def __init__(self, person1: Person, person2: Person):
        self.person1 = person1
        self.person2 = person2
        self.shared_goals: List[SharedGoal] = []
        self.split_type = SplitType.EQUAL
    
    def get_combined_finances(self) -> Dict[str, Any]:
        """Get combined financial snapshot"""
        return {
            "combined_income": self.person1.income + self.person2.income,
            "combined_expenses": self.person1.expenses + self.person2.expenses,
            "combined_savings": self.person1.savings + self.person2.savings,
            "combined_debt": self.person1.debt + self.person2.debt,
            "combined_investments": self.person1.investments + self.person2.investments,
            "net_worth": (
                self.person1.savings + self.person2.savings + 
                self.person1.investments + self.person2.investments - 
                self.person1.debt - self.person2.debt
            ),
            "savings_rate": self._calculate_savings_rate(),
            "income_ratio": {
                self.person1.name: round(self.person1.income / (self.person1.income + self.person2.income), 2) if self.person1.income + self.person2.income > 0 else 0.5,
                self.person2.name: round(self.person2.income / (self.person1.income + self.person2.income), 2) if self.person1.income + self.person2.income > 0 else 0.5
            }
        }
    
    def _calculate_savings_rate(self) -> float:
        """Calculate combined savings rate"""
        total_income = self.person1.income + self.person2.income
        if total_income == 0:
            return 0
        
        total_savings = self.person1.savings + self.person2.savings
        return round((total_savings / total_income) * 100, 2)
    
    def suggest_expense_split(
        self, 
        total_expense: float,
        split_type: SplitType = SplitType.PROPORTIONAL,
        custom_split: Optional[Dict[str, float]] = None
    ) -> Dict[str, float]:
        """Suggest how to split expenses"""
        
        if split_type == SplitType.EQUAL:
            return {
                self.person1.name: round(total_expense / 2, 2),
                self.person2.name: round(total_expense / 2, 2)
            }
        
        elif split_type == SplitType.PROPORTIONAL:
            total_income = self.person1.income + self.person2.income
            if total_income == 0:
                return {self.person1.name: 0, self.person2.name: 0}
            
            p1_ratio = self.person1.income / total_income
            p2_ratio = self.person2.income / total_income
            
            return {
                self.person1.name: round(total_expense * p1_ratio, 2),
                self.person2.name: round(total_expense * p2_ratio, 2)
            }
        
        elif split_type == SplitType.CUSTOM and custom_split:
            return {
                self.person1.name: round(total_expense * custom_split.get(self.person1.name, 0.5), 2),
                self.person2.name: round(total_expense * custom_split.get(self.person2.name, 0.5), 2)
            }
        
        return {self.person1.name: total_expense / 2, self.person2.name: total_expense / 2}
    
    def add_shared_goal(
        self,
        name: str,
        target_amount: float,
        deadline_years: int,
        priority: int = 3,
        split_type: SplitType = SplitType.PROPORTIONAL
    ) -> SharedGoal:
        """Add a shared financial goal"""
        
        total_income = self.person1.income + self.person2.income
        
        if split_type == SplitType.EQUAL or total_income == 0:
            contribution_split = {
                self.person1.name: 0.5,
                self.person2.name: 0.5
            }
        else:
            p1_ratio = self.person1.income / total_income
            p2_ratio = self.person2.income / total_income
            contribution_split = {
                self.person1.name: round(p1_ratio, 2),
                self.person2.name: round(p2_ratio, 2)
            }
        
        goal = SharedGoal(
            name=name,
            target_amount=target_amount,
            deadline_years=deadline_years,
            priority=priority,
            contribution_split=contribution_split
        )
        
        self.shared_goals.append(goal)
        return goal
    
    def calculate_sip_for_goals(
        self,
        expected_return: float = 0.12
    ) -> Dict[str, Any]:
        """Calculate SIP required for each goal"""
        
        results = []
        total_monthly_sip = 0
        
        for goal in self.shared_goals:
            # Calculate future value with inflation
            inflation = 0.06  # 6% inflation
            future_value = goal.target_amount * ((1 + inflation) ** goal.deadline_years)
            
            # Calculate monthly SIP
            monthly_rate = expected_return / 12
            months = goal.deadline_years * 12
            
            if months <= 0:
                sip_needed = future_value
            else:
                sip_needed = future_value * monthly_rate / ((1 + monthly_rate) ** months - 1)
            
            # Split by contribution
            person1_contribution = sip_needed * goal.contribution_split.get(self.person1.name, 0.5)
            person2_contribution = sip_needed * goal.contribution_split.get(self.person2.name, 0.5)
            
            results.append({
                "goal": goal.name,
                "target_amount": goal.target_amount,
                "inflation_adjusted": round(future_value, 2),
                "deadline_years": goal.deadline_years,
                "priority": goal.priority,
                "total_monthly_sip": round(sip_needed, 2),
                "contributions": {
                    self.person1.name: round(person1_contribution, 2),
                    self.person2.name: round(person2_contribution, 2)
                }
            })
            
            total_monthly_sip += sip_needed
        
        # Calculate affordability for each person
        p1_affordability = self._check_affordability(
            self.person1,
            sum(r["contributions"][self.person1.name] for r in results)
        )
        p2_affordability = self._check_affordability(
            self.person2,
            sum(r["contributions"][self.person2.name] for r in results)
        )
        
        return {
            "goals": results,
            "total_monthly_sip": round(total_monthly_sip, 2),
            "contributions_by_person": {
                self.person1.name: round(sum(r["contributions"][self.person1.name] for r in results), 2),
                self.person2.name: round(sum(r["contributions"][self.person2.name] for r in results), 2)
            },
            "affordability": {
                self.person1.name: p1_affordability,
                self.person2.name: p2_affordability
            }
        }
    
    def _check_affordability(self, person: Person, monthly_investment: float) -> Dict[str, Any]:
        """Check if monthly investment is affordable"""
        savings_capacity = person.income * 0.3  # 30% savings rate
        current_savings = person.savings if person.savings > 0 else person.income * 0.2
        
        return {
            "monthly_investment": round(monthly_investment, 2),
            "savings_capacity": round(savings_capacity, 2),
            "current_monthly_savings": round(current_savings, 2),
            "is_affordable": monthly_investment <= savings_capacity,
            "buffer": round(savings_capacity - monthly_investment, 2)
        }
    
    def create_budget_plan(
        self,
        categories: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """Create a joint budget plan using 50/30/20 rule"""
        
        combined = self.get_combined_finances()
        total_income = combined["combined_income"]
        
        # Default categories
        if categories is None:
            categories = [
                {"name": "Housing", "type": "needs", "percentage": 30},
                {"name": "Food & Groceries", "type": "needs", "percentage": 15},
                {"name": "Transportation", "type": "needs", "percentage": 10},
                {"name": "Utilities", "type": "needs", "percentage": 5},
                {"name": "Healthcare", "type": "needs", "percentage": 5},
                {"name": "Entertainment", "type": "wants", "percentage": 10},
                {"name": "Shopping", "type": "wants", "percentage": 10},
                {"name": "Dining Out", "type": "wants", "percentage": 5},
                {"name": "Emergency Fund", "type": "savings", "percentage": 5},
                {"name": "Investments", "type": "savings", "percentage": 10},
                {"name": "Goals", "type": "savings", "percentage": 5}
            ]
        
        # Calculate amounts
        budget = {"needs": 0, "wants": 0, "savings": 0}
        detailed_budget = []
        
        for cat in categories:
            amount = round(total_income * cat["percentage"] / 100, 2)
            split = self.suggest_expense_split(amount, SplitType.PROPORTIONAL)
            
            detailed_budget.append({
                "category": cat["name"],
                "type": cat["type"],
                "percentage": cat["percentage"],
                "amount": amount,
                "split": split
            })
            
            budget[cat["type"]] += amount
        
        return {
            "total_income": total_income,
            "income_split": combined["income_ratio"],
            "summary": {
                "needs": round(budget["needs"], 2),
                "wants": round(budget["wants"], 2),
                "savings": round(budget["savings"], 2),
                "needs_percentage": round((budget["needs"] / total_income) * 100, 1),
                "wants_percentage": round((budget["wants"] / total_income) * 100, 1),
                "savings_percentage": round((budget["savings"] / total_income) * 100, 1)
            },
            "categories": detailed_budget,
            "recommendations": self._generate_budget_recommendations(budget, total_income)
        }
    
    def _generate_budget_recommendations(
        self, 
        budget: Dict[str, float], 
        income: float
    ) -> List[str]:
        """Generate budget recommendations"""
        recommendations = []
        
        needs_pct = (budget["needs"] / income) * 100
        wants_pct = (budget["wants"] / income) * 100
        savings_pct = (budget["savings"] / income) * 100
        
        if needs_pct > 50:
            recommendations.append(f"Needs ({needs_pct:.1f}%) exceed 50% of income. Consider reducing housing costs.")
        
        if wants_pct > 30:
            recommendations.append(f"Wants ({wants_pct:.1f}%) exceed 30% of income. Consider reducing discretionary spending.")
        
        if savings_pct < 20:
            recommendations.append(f"Savings ({savings_pct:.1f}%) below recommended 20%. Try to increase savings rate.")
        
        if savings_pct >= 20:
            recommendations.append("Good savings rate! Consider investing in tax-advantaged accounts.")
        
        # Couple-specific recommendations
        income_diff = abs(self.person1.income - self.person2.income)
        if income_diff > (self.person1.income + self.person2.income) * 0.3:
            recommendations.append("Large income disparity. Consider proportional expense splitting.")
        
        return recommendations
    
    def plan_debt_payoff(
        self,
        debts: List[Dict[str, Any]],
        strategy: str = "avalanche"  # avalanche or snowball
    ) -> Dict[str, Any]:
        """Plan debt payoff strategy for couple"""
        
        # Combine debts from both persons
        combined_debts = []
        for debt in debts:
            combined_debts.append({
                "name": debt["name"],
                "amount": debt["amount"],
                "interest_rate": debt.get("interest_rate", 12),
                "min_payment": debt.get("min_payment", debt["amount"] * 0.03),
                "owner": debt.get("owner", "joint")
            })
        
        # Sort by strategy
        if strategy == "avalanche":  # Highest interest first
            combined_debts.sort(key=lambda x: x["interest_rate"], reverse=True)
        else:  # snowball - smallest balance first
            combined_debts.sort(key=lambda x: x["amount"])
        
        # Calculate payoff timeline
        total_debt = sum(d["amount"] for d in combined_debts)
        total_min_payment = sum(d["min_payment"] for d in combined_debts)
        
        # Extra payment capacity (30% of combined savings)
        combined = self.get_combined_finances()
        extra_payment = combined["combined_income"] * 0.1  # 10% extra
        
        payoff_plan = []
        remaining_debts = combined_debts.copy()
        months = 0
        
        while remaining_debts and months < 120:  # Max 10 years
            months += 1
            for debt in remaining_debts:
                interest = debt["amount"] * (debt["interest_rate"] / 100 / 12)
                debt["amount"] += interest
            
            # Make payments
            payment_remaining = total_min_payment + extra_payment
            for i, debt in enumerate(remaining_debts):
                payment = min(debt["amount"], payment_remaining)
                debt["amount"] -= payment
                payment_remaining -= payment
            
            # Remove paid debts
            remaining_debts = [d for d in remaining_debts if d["amount"] > 0]
        
        # Split responsibility
        debt_by_owner = {"joint": 0, self.person1.name: 0, self.person2.name: 0}
        for debt in combined_debts:
            owner = debt.get("owner", "joint")
            if owner in debt_by_owner:
                debt_by_owner[owner] += debt["amount"]
        
        return {
            "strategy": strategy,
            "total_debt": round(total_debt, 2),
            "debt_by_owner": {k: round(v, 2) for k, v in debt_by_owner.items()},
            "total_min_payment": round(total_min_payment, 2),
            "extra_payment_capacity": round(extra_payment, 2),
            "estimated_payoff_months": months,
            "payoff_order": [d["name"] for d in combined_debts],
            "recommendations": [
                f"Use {strategy} method for optimal payoff",
                "Allocate extra payments to highest priority debt",
                "Consider balance transfer for high-interest debts"
            ]
        }


# Convenience functions for API
def create_couple_plan(
    person1_name: str,
    person1_income: float,
    person2_name: str,
    person2_income: float,
    goals: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """Create a comprehensive couple financial plan"""
    
    p1 = Person(name=person1_name, income=person1_income)
    p2 = Person(name=person2_name, income=person2_income)
    
    planner = CouplePlanner(p1, p2)
    
    # Add default goals if none provided
    if goals:
        for goal in goals:
            planner.add_shared_goal(
                name=goal["name"],
                target_amount=goal["target_amount"],
                deadline_years=goal["years"],
                priority=goal.get("priority", 3)
            )
    
    return {
        "combined_finances": planner.get_combined_finances(),
        "budget_plan": planner.create_budget_plan(),
        "goal_sip_calculation": planner.calculate_sip_for_goals() if goals else None
    }

def calculate_expense_split(
    person1_name: str,
    person1_income: float,
    person2_name: str,
    person2_income: float,
    expense_amount: float,
    split_type: str = "proportional"
) -> Dict[str, float]:
    """Calculate how a couple should split an expense"""
    
    p1 = Person(name=person1_name, income=person1_income)
    p2 = Person(name=person2_name, income=person2_income)
    
    planner = CouplePlanner(p1, p2)
    split_enum = SplitType(split_type)
    
    return planner.suggest_expense_split(expense_amount, split_enum)