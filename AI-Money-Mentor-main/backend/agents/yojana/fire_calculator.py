"""
FIRE (Financial Independence, Retire Early) Calculator
Indian market-focused retirement planning
"""

import math
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class FIREMethod(Enum):
    """FIRE calculation methods"""
    FOUR_PERCENT = "4% Rule"  # Classic FIRE
    THREE_PERCENT = "3% Rule"  # Conservative
    FIVE_PERCENT = "5% Rule"  # Aggressive


@dataclass
class FIREPlan:
    """FIRE retirement plan"""
    fire_number: float  # Target corpus
    monthly_savings: float
    years_to_fire: int
    monthly_expenses: float
    withdrawal_rate: float
    inflation_adjusted_corpus: float
    sip_breakdown: List[Dict]


class FIRECalculator:
    """
    FIRE Calculator for Indian investors
    
    Features:
    - Calculate FIRE number based on expenses
    - SIP roadmap generator
    - Inflation-adjusted projections
    - Multiple withdrawal strategies
    """
    
    # Indian context defaults
    DEFAULT_INFLATION = 0.06  # 6% average inflation in India
    DEFAULT_RETURN = 0.12    # 12% average equity return (long-term)
    DEFAULT_DEBT_RETURN = 0.07  # 7% debt fund return
    
    def __init__(
        self,
        monthly_expenses: float,
        current_age: int,
        retirement_age: int,
        current_corpus: float = 0,
        inflation_rate: float = DEFAULT_INFLATION,
        expected_return: float = DEFAULT_RETURN,
        withdrawal_rate: float = 0.04,
        equity_allocation: float = 0.70
    ):
        """
        Initialize FIRE calculator
        
        Args:
            monthly_expenses: Current monthly expenses (₹)
            current_age: Current age
            retirement_age: Target retirement age
            current_corpus: Existing investments (₹)
            inflation_rate: Expected inflation rate (default 6%)
            expected_return: Expected investment return (default 12%)
            withdrawal_rate: Safe withdrawal rate (default 4%)
            equity_allocation: Equity allocation % (default 70%)
        """
        self.monthly_expenses = monthly_expenses
        self.current_age = current_age
        self.retirement_age = retirement_age
        self.current_corpus = current_corpus
        self.inflation_rate = inflation_rate
        self.expected_return = expected_return
        self.withdrawal_rate = withdrawal_rate
        self.equity_allocation = equity_allocation
        
    def calculate_fire_number(self) -> float:
        """
        Calculate FIRE number (target corpus)
        
        Formula: Annual Expenses / Withdrawal Rate
        
        For 4% rule: Corpus = Annual Expenses / 0.04
        For 3% rule: Corpus = Annual Expenses / 0.03
        
        Returns:
            Target corpus amount
        """
        annual_expenses = self.monthly_expenses * 12
        return annual_expenses / self.withdrawal_rate
    
    def calculate_inflation_adjusted_corpus(self) -> float:
        """
        Calculate inflation-adjusted corpus needed at retirement
        
        Future Value = Present Value × (1 + inflation)^years
        
        Returns:
            Inflation-adjusted target corpus
        """
        years_to_retirement = self.retirement_age - self.current_age
        annual_expenses = self.monthly_expenses * 12
        
        # Inflate expenses to retirement age
        inflated_expenses = annual_expenses * ((1 + self.inflation_rate) ** years_to_retirement)
        
        # FIRE number based on inflated expenses
        return inflated_expenses / self.withdrawal_rate
    
    def calculate_years_to_fire(self, monthly_savings: float) -> int:
        """
        Calculate years to reach FIRE
        
        Uses compound interest formula with monthly contributions
        
        FV = P × (1+r)^n + PMT × [((1+r)^n - 1) / r]
        
        Args:
            monthly_savings: Monthly SIP amount
            
        Returns:
            Years to reach FIRE
        """
        target_corpus = self.calculate_inflation_adjusted_corpus() - self.current_corpus
        monthly_return = self.expected_return / 12
        
        if monthly_savings <= 0:
            return float('inf')
        
        # Solve for n using numerical approximation
        corpus = self.current_corpus
        months = 0
        max_months = 600  # 50 years max
        
        while corpus < target_corpus and months < max_months:
            corpus = corpus * (1 + monthly_return) + monthly_savings
            months += 1
        
        return months // 12  # Convert to years
    
    def calculate_monthly_savings(self, years: int = None) -> float:
        """
        Calculate required monthly savings to reach FIRE
        
        Uses PMT formula derived from compound interest
        
        Args:
            target_years: Target years to FIRE (if None, use retirement age)
            
        Returns:
            Required monthly SIP amount
        """
        target_years = years if years is not None else self.retirement_age - self.current_age
        
        target_corpus = self.calculate_inflation_adjusted_corpus() - self.current_corpus
        monthly_return = self.expected_return / 12
        months = target_years * 12
        
        if months <= 0:
            return target_corpus  # Already at FIRE
        
        # PMT formula
        # PMT = FV × r / ((1+r)^n - 1)
        
        # With initial corpus
        # PMT = (FV - PV × (1+r)^n) × r / ((1+r)^n - 1)
        
        fv_factor = (1 + monthly_return) ** months
        pmt = (target_corpus - self.current_corpus * fv_factor) * monthly_return / (fv_factor - 1)
        
        return max(0, pmt)
    
    def generate_sip_roadmap(self, years: int) -> List[Dict]:
        """
        Generate year-by-year SIP roadmap
        
        Args:
            years: Number of years to project
            
        Returns:
            List of yearly projections
        """
        roadmap = []
        corpus = self.current_corpus
        monthly_savings = self.calculate_monthly_savings(years)
        annual_return = self.expected_return
        
        for year in range(1, years + 1):
            # Calculate corpus at end of year
            for month in range(12):
                corpus = corpus * (1 + annual_return / 12) + monthly_savings
            
            # Calculate inflation-adjusted expenses
            inflated_expenses = self.monthly_expenses * ((1 + self.inflation_rate) ** year)
            
            # Calculate FIRE progress
            fire_number = inflated_expenses * 12 / self.withdrawal_rate
            progress = (corpus / fire_number) * 100
            
            roadmap.append({
                'year': year,
                'age': self.current_age + year,
                'corpus': round(corpus, 0),
                'monthly_savings': round(monthly_savings, 0),
                'annual_investment': round(monthly_savings * 12, 0),
                'inflated_expenses': round(inflated_expenses, 0),
                'fire_number': round(fire_number, 0),
                'progress': round(progress, 1),
                'total_invested': round(self.current_corpus + monthly_savings * 12 * year, 0)
            })
        
        return roadmap
    
    def calculate_goal_based_sip(
        self,
        goals: List[Dict],
        years: int
    ) -> Dict:
        """
        Calculate SIP for multiple financial goals
        
        Args:
            goals: List of goals with target_amount, years, priority
            years: Total investment horizon
            
        Returns:
            Goal-based SIP allocation
        """
        total_required = 0
        goal_allocation = []
        
        for goal in goals:
            target = goal.get('target_amount', 0)
            goal_years = goal.get('years', years)
            priority = goal.get('priority', 1)
            
            # Calculate monthly SIP for this goal
            monthly_return = self.expected_return / 12
            months = goal_years * 12
            
            if months > 0:
                pmt = target * monthly_return / ((1 + monthly_return) ** months - 1)
            else:
                pmt = target / 12
            
            # Adjust for priority (higher priority = more allocation)
            adjusted_pmt = pmt * (2 - priority * 0.1)
            
            total_required += adjusted_pmt
            
            goal_allocation.append({
                'goal': goal.get('name', 'Unknown'),
                'target': target,
                'monthly_sip': round(adjusted_pmt, 0),
                'years': goal_years,
                'priority': priority
            })
        
        return {
            'total_monthly_sip': round(total_required, 0),
            'goals': goal_allocation
        }
    
    def get_fire_plan(self, monthly_savings: Optional[float] = None) -> FIREPlan:
        """
        Get complete FIRE plan
        
        Args:
            monthly_savings: Optional monthly savings (if None, calculate automatically)
            
        Returns:
            FIREPlan object with all details
        """
        fire_number = self.calculate_fire_number()
        inflation_adjusted = self.calculate_inflation_adjusted_corpus()
        
        if monthly_savings is None:
            monthly_savings = self.calculate_monthly_savings()
        
        years_to_fire = self.calculate_years_to_fire(monthly_savings)
        roadmap = self.generate_sip_roadmap(max(1, years_to_fire))
        
        return FIREPlan(
            fire_number=round(fire_number, 0),
            monthly_savings=round(monthly_savings, 0),
            years_to_fire=years_to_fire,
            monthly_expenses=self.monthly_expenses,
            withdrawal_rate=self.withdrawal_rate * 100,
            inflation_adjusted_corpus=round(inflation_adjusted, 0),
            sip_breakdown=roadmap
        )


# Indian FIRE specific functions
def calculate_fire_number_india(
    monthly_expenses: float,
    withdrawal_rate: float = 0.04,
    inflation: float = 0.06
) -> Dict:
    """
    Calculate FIRE number for Indian context
    
    Args:
        monthly_expenses: Current monthly expenses in ₹
        withdrawal_rate: Safe withdrawal rate (default 4%)
        inflation: Expected inflation in India (default 6%)
        
    Returns:
        Dictionary with FIRE calculations
    """
    annual_expenses = monthly_expenses * 12
    
    # Classic FIRE
    classic_fire = annual_expenses / withdrawal_rate
    
    # Conservative FIRE (3% withdrawal)
    conservative_fire = annual_expenses / 0.03
    
    # Aggressive FIRE (5% withdrawal)
    aggressive_fire = annual_expenses / 0.05
    
    # Lean FIRE (minimal expenses)
    lean_fire = (monthly_expenses * 0.7 * 12) / withdrawal_rate
    
    # Fat FIRE (comfortable expenses)
    fat_fire = (monthly_expenses * 1.5 * 12) / withdrawal_rate
    
    return {
        'classic_fire': round(classic_fire, 0),
        'conservative_fire': round(conservative_fire, 0),
        'aggressive_fire': round(aggressive_fire, 0),
        'lean_fire': round(lean_fire, 0),
        'fat_fire': round(fat_fire, 0),
        'annual_expenses': annual_expenses,
        'monthly_expenses': monthly_expenses,
        'withdrawal_rate': f"{withdrawal_rate * 100}%"
    }


def get_sip_recommendation(
    target_corpus: float,
    years: int,
    expected_return: float = 0.12
) -> Dict:
    """
    Get SIP recommendation for target corpus
    
    Args:
        target_corpus: Target amount in ₹
        years: Investment horizon in years
        expected_return: Expected annual return (default 12%)
        
    Returns:
        SIP recommendation details
    """
    monthly_return = expected_return / 12
    months = years * 12
    
    if months <= 0:
        return {'error': 'Invalid time horizon'}
    
    # SIP formula: PMT = FV × r / ((1+r)^n - 1)
    fv_factor = (1 + monthly_return) ** months
    monthly_sip = target_corpus * monthly_return / (fv_factor - 1)
    
    # Lumpsum alternative
    lumpsum = target_corpus / fv_factor
    
    # Different scenarios
    scenarios = {}
    for rate in [0.08, 0.10, 0.12, 0.14, 0.16]:
        mr = rate / 12
        ff = (1 + mr) ** months
        scenarios[f'{rate*100:.0f}%'] = round(target_corpus * mr / (ff - 1), 0)
    
    return {
        'monthly_sip': round(monthly_sip, 0),
        'annual_investment': round(monthly_sip * 12, 0),
        'lumpsum_alternative': round(lumpsum, 0),
        'total_investment': round(monthly_sip * months, 0),
        'expected_corpus': round(target_corpus, 0),
        'years': years,
        'return_rate': f"{expected_return * 100}%",
        'scenarios': scenarios
    }
