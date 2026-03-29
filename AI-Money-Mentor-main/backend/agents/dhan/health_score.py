"""
Financial Health Score Calculator
Comprehensive financial health assessment for Indian users
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class HealthCategory(Enum):
    """Financial health categories"""
    EMERGENCY_FUND = "Emergency Fund"
    DEBT_RATIO = "Debt to Income"
    SAVINGS_RATE = "Savings Rate"
    INVESTMENT_RATIO = "Investment Ratio"
    INSURANCE_COVERAGE = "Insurance Coverage"
    RETIREMENT_READINESS = "Retirement Readiness"
    CREDIT_SCORE = "Credit Score"
    EXPENSE_RATIO = "Expense Ratio"


@dataclass
class HealthMetric:
    """Individual health metric"""
    category: str
    score: float  # 0-100
    weight: float  # Importance weight
    status: str  # 'excellent', 'good', 'fair', 'poor', 'critical'
    message: str
    suggestion: str


@dataclass
class HealthReport:
    """Complete health report"""
    overall_score: float
    grade: str  # A+, A, B, C, D, F
    metrics: List[HealthMetric]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    monthly_surplus: float
    financial_age: int  # "Financial age" based on habits


class FinancialHealthCalculator:
    """
    Calculate comprehensive financial health score
    
    Based on Indian financial context:
    - Emergency fund (6 months expenses)
    - Debt-to-income ratio
    - Savings rate
    - Investment allocation
    - Insurance coverage
    - Retirement planning
    """
    
    # Indian context weights (total = 1.0)
    WEIGHTS = {
        HealthCategory.EMERGENCY_FUND: 0.15,
        HealthCategory.DEBT_RATIO: 0.15,
        HealthCategory.SAVINGS_RATE: 0.20,
        HealthCategory.INVESTMENT_RATIO: 0.20,
        HealthCategory.INSURANCE_COVERAGE: 0.10,
        HealthCategory.RETIREMENT_READINESS: 0.10,
        HealthCategory.CREDIT_SCORE: 0.05,
        HealthCategory.EXPENSE_RATIO: 0.05
    }
    
    def __init__(
        self,
        monthly_income: float,
        monthly_expenses: float,
        monthly_emi: float = 0,
        monthly_savings: float = 0,
        monthly_investments: float = 0,
        emergency_fund: float = 0,
        life_insurance_cover: float = 0,
        health_insurance_cover: float = 0,
        retirement_corpus: float = 0,
        age: int = 30,
        credit_score: int = 750,
        dependents: int = 0
    ):
        """
        Initialize financial health calculator
        
        Args:
            monthly_income: Gross monthly income (₹)
            monthly_expenses: Monthly expenses (₹)
            monthly_emi: Monthly EMI payments (₹)
            monthly_savings: Monthly savings (₹)
            monthly_investments: Monthly investments (₹)
            emergency_fund: Current emergency fund (₹)
            life_insurance_cover: Life insurance coverage (₹)
            health_insurance_cover: Health insurance coverage (₹)
            retirement_corpus: Current retirement corpus (₹)
            age: Current age
            credit_score: Credit score (300-900)
            dependents: Number of dependents
        """
        self.monthly_income = monthly_income
        self.monthly_expenses = monthly_expenses
        self.monthly_emi = monthly_emi
        self.monthly_savings = monthly_savings
        self.monthly_investments = monthly_investments
        self.emergency_fund = emergency_fund
        self.life_insurance_cover = life_insurance_cover
        self.health_insurance_cover = health_insurance_cover
        self.retirement_corpus = retirement_corpus
        self.age = age
        self.credit_score = credit_score
        self.dependents = dependents
    
    def _get_status(self, score: float) -> tuple:
        """Get status and message based on score"""
        if score >= 80:
            return 'excellent', '🌟 Excellent!'
        elif score >= 60:
            return 'good', '✅ Good'
        elif score >= 40:
            return 'fair', '⚠️ Needs Improvement'
        elif score >= 20:
            return 'poor', '❌ Poor'
        else:
            return 'critical', '🚨 Critical!'
    
    def calculate_emergency_fund_score(self) -> HealthMetric:
        """
        Calculate emergency fund score
        
        Ideal: 6 months of expenses
        Score = (months_covered / 6) * 100
        """
        monthly_needs = self.monthly_expenses + self.monthly_emi
        months_covered = self.emergency_fund / monthly_needs if monthly_needs > 0 else 0
        
        # Cap at 12 months for score calculation
        score = min(100, (months_covered / 6) * 100)
        status, emoji = self._get_status(score)
        
        if months_covered >= 6:
            message = f"Emergency fund covers {months_covered:.1f} months"
            suggestion = "Consider investing excess in liquid funds for better returns"
        elif months_covered >= 3:
            message = f"Emergency fund covers {months_covered:.1f} months (needs 6)"
            suggestion = "Increase emergency fund to cover 6 months of expenses"
        else:
            message = f"Emergency fund only covers {months_covered:.1f} months"
            suggestion = f"Urgently build emergency fund of ₹{monthly_needs * 6:,.0f}"
        
        return HealthMetric(
            category=HealthCategory.EMERGENCY_FUND.value,
            score=score,
            weight=self.WEIGHTS[HealthCategory.EMERGENCY_FUND],
            status=status,
            message=message,
            suggestion=suggestion
        )
    
    def calculate_debt_ratio_score(self) -> HealthMetric:
        """
        Calculate debt-to-income ratio score
        
        Ideal: <30% of income
        Score based on ratio: 0% = 100, 30% = 80, 50% = 40, >70% = 0
        """
        if self.monthly_income == 0:
            return HealthMetric(
                category=HealthCategory.DEBT_RATIO.value,
                score=0,
                weight=self.WEIGHTS[HealthCategory.DEBT_RATIO],
                status='critical',
                message="No income data",
                suggestion="Add income information"
            )
        
        debt_ratio = (self.monthly_emi / self.monthly_income) * 100
        
        # Score calculation
        if debt_ratio <= 20:
            score = 100
        elif debt_ratio <= 30:
            score = 90
        elif debt_ratio <= 40:
            score = 70
        elif debt_ratio <= 50:
            score = 50
        elif debt_ratio <= 60:
            score = 30
        else:
            score = 10
        
        status, emoji = self._get_status(score)
        
        if debt_ratio <= 30:
            message = f"Debt-to-income ratio: {debt_ratio:.1f}% (healthy)"
            suggestion = "Maintain low debt levels for financial flexibility"
        elif debt_ratio <= 50:
            message = f"Debt-to-income ratio: {debt_ratio:.1f}% (moderate)"
            suggestion = "Consider prepaying loans to reduce EMI burden"
        else:
            message = f"Debt-to-income ratio: {debt_ratio:.1f}% (high risk)"
            suggestion = "Reduce debt aggressively. Consider balance transfer or restructuring"
        
        return HealthMetric(
            category=HealthCategory.DEBT_RATIO.value,
            score=score,
            weight=self.WEIGHTS[HealthCategory.DEBT_RATIO],
            status=status,
            message=message,
            suggestion=suggestion
        )
    
    def calculate_savings_rate_score(self) -> HealthMetric:
        """
        Calculate savings rate score
        
        Ideal: 20-30% of income
        Indian benchmark: Save at least 20% for goals
        """
        if self.monthly_income == 0:
            return HealthMetric(
                category=HealthCategory.SAVINGS_RATE.value,
                score=0,
                weight=self.WEIGHTS[HealthCategory.SAVINGS_RATE],
                status='critical',
                message="No income data",
                suggestion="Add income information"
            )
        
        total_savings = self.monthly_savings + self.monthly_investments
        savings_rate = (total_savings / self.monthly_income) * 100
        
        # Score calculation
        if savings_rate >= 30:
            score = 100
        elif savings_rate >= 20:
            score = 85
        elif savings_rate >= 15:
            score = 70
        elif savings_rate >= 10:
            score = 50
        elif savings_rate >= 5:
            score = 30
        else:
            score = 10
        
        status, emoji = self._get_status(score)
        
        if savings_rate >= 20:
            message = f"Savings rate: {savings_rate:.1f}% (excellent)"
            suggestion = "Consider increasing investment allocation"
        elif savings_rate >= 10:
            message = f"Savings rate: {savings_rate:.1f}% (needs improvement)"
            suggestion = f"Aim to save ₹{self.monthly_income * 0.2:,.0f}/month (20% of income)"
        else:
            message = f"Savings rate: {savings_rate:.1f}% (critical)"
            suggestion = "Cut expenses, increase income. Target 20% savings rate"
        
        return HealthMetric(
            category=HealthCategory.SAVINGS_RATE.value,
            score=score,
            weight=self.WEIGHTS[HealthCategory.SAVINGS_RATE],
            status=status,
            message=message,
            suggestion=suggestion
        )
    
    def calculate_investment_ratio_score(self) -> HealthMetric:
        """
        Calculate investment ratio score
        
        Measures what % of savings goes to investments
        Ideal: 80%+ of savings should be invested
        """
        total_savings = self.monthly_savings + self.monthly_investments
        
        if total_savings == 0:
            return HealthMetric(
                category=HealthCategory.INVESTMENT_RATIO.value,
                score=0,
                weight=self.WEIGHTS[HealthCategory.INVESTMENT_RATIO],
                status='critical',
                message="No savings to invest",
                suggestion="Start saving before investing"
            )
        
        investment_ratio = (self.monthly_investments / total_savings) * 100
        
        # Score calculation
        if investment_ratio >= 80:
            score = 100
        elif investment_ratio >= 60:
            score = 80
        elif investment_ratio >= 40:
            score = 60
        elif investment_ratio >= 20:
            score = 40
        else:
            score = 20
        
        status, emoji = self._get_status(score)
        
        if investment_ratio >= 60:
            message = f"Investment ratio: {investment_ratio:.1f}% (good)"
            suggestion = "Continue systematic investing. Review asset allocation"
        else:
            message = f"Investment ratio: {investment_ratio:.1f}% (low)"
            suggestion = "Move savings to investments. Idle cash loses value to inflation"
        
        return HealthMetric(
            category=HealthCategory.INVESTMENT_RATIO.value,
            score=score,
            weight=self.WEIGHTS[HealthCategory.INVESTMENT_RATIO],
            status=status,
            message=message,
            suggestion=suggestion
        )
    
    def calculate_insurance_score(self) -> HealthMetric:
        """
        Calculate insurance coverage score
        
        Life insurance: 10x annual income (or 15x if young)
        Health insurance: ₹5-10 lakhs minimum
        """
        annual_income = self.monthly_income * 12
        recommended_life_cover = annual_income * max(10, 15 - self.age // 10)
        
        # Life insurance score (0-50)
        life_cover_ratio = self.life_insurance_cover / recommended_life_cover if recommended_life_cover > 0 else 0
        life_score = min(50, life_cover_ratio * 50)
        
        # Health insurance score (0-50)
        recommended_health = 1000000  # ₹10 lakhs minimum
        health_cover_ratio = self.health_insurance_cover / recommended_health
        health_score = min(50, health_cover_ratio * 50)
        
        total_score = life_score + health_score
        status, emoji = self._get_status(total_score)
        
        life_msg = f"Life: ₹{self.life_insurance_cover/100000:.0f}L (need ₹{recommended_life_cover/100000:.0f}L)"
        health_msg = f"Health: ₹{self.health_insurance_cover/100000:.0f}L (need ₹10L)"
        
        if total_score >= 80:
            suggestion = "Well insured. Review annually"
        else:
            suggestion = f"Increase life cover to ₹{recommended_life_cover/100000:.0f}L and health to ₹10L"
        
        return HealthMetric(
            category=HealthCategory.INSURANCE_COVERAGE.value,
            score=total_score,
            weight=self.WEIGHTS[HealthCategory.INSURANCE_COVERAGE],
            status=status,
            message=f"{life_msg}, {health_msg}",
            suggestion=suggestion
        )
    
    def calculate_retirement_score(self) -> HealthMetric:
        """
        Calculate retirement readiness score
        
        Based on:
        - Current corpus vs needed corpus
        - Monthly investment vs required SIP
        - Years to retirement
        """
        retirement_age = 60
        years_to_retire = max(0, retirement_age - self.age)
        
        # Calculate required corpus (25x annual expenses at retirement)
        future_expenses = self.monthly_expenses * 12 * (1.06 ** years_to_retire)  # 6% inflation
        required_corpus = future_expenses * 25
        
        # Current corpus score
        corpus_ratio = self.retirement_corpus / required_corpus if required_corpus > 0 else 0
        corpus_score = min(50, corpus_ratio * 50)
        
        # Monthly investment score
        required_monthly = required_corpus * (0.12 / 12) / ((1 + 0.12 / 12) ** (years_to_retire * 12) - 1)
        investment_ratio = self.monthly_investments / required_monthly if required_monthly > 0 else 0
        investment_score = min(50, investment_ratio * 50)
        
        total_score = corpus_score + investment_score
        status, emoji = self._get_status(total_score)
        
        if total_score >= 60:
            suggestion = "On track for retirement. Review asset allocation"
        else:
            suggestion = f"Increase monthly investment to ₹{required_monthly:,.0f} for retirement"
        
        return HealthMetric(
            category=HealthCategory.RETIREMENT_READINESS.value,
            score=total_score,
            weight=self.WEIGHTS[HealthCategory.RETIREMENT_READINESS],
            status=status,
            message=f"Corpus: ₹{self.retirement_corpus/100000:.1f}L / ₹{required_corpus/100000:.0f}L needed",
            suggestion=suggestion
        )
    
    def calculate_credit_score_metric(self) -> HealthMetric:
        """
        Calculate credit score metric
        
        Indian credit score range: 300-900
        Good: 750+
        """
        if self.credit_score >= 800:
            score = 100
            status = 'excellent'
        elif self.credit_score >= 750:
            score = 85
            status = 'good'
        elif self.credit_score >= 700:
            score = 70
            status = 'fair'
        elif self.credit_score >= 650:
            score = 50
            status = 'poor'
        else:
            score = 20
            status = 'critical'
        
        if self.credit_score >= 750:
            suggestion = "Maintain good credit habits. Check score annually"
        else:
            suggestion = "Improve credit score: pay bills on time, reduce credit utilization"
        
        return HealthMetric(
            category=HealthCategory.CREDIT_SCORE.value,
            score=score,
            weight=self.WEIGHTS[HealthCategory.CREDIT_SCORE],
            status=status,
            message=f"Credit score: {self.credit_score}/900",
            suggestion=suggestion
        )
    
    def calculate_expense_ratio_score(self) -> HealthMetric:
        """
        Calculate expense ratio score
        
        Measures what % of income goes to expenses
        Lower is better (more room for savings)
        """
        if self.monthly_income == 0:
            return HealthMetric(
                category=HealthCategory.EXPENSE_RATIO.value,
                score=0,
                weight=self.WEIGHTS[HealthCategory.EXPENSE_RATIO],
                status='critical',
                message="No income data",
                suggestion="Add income information"
            )
        
        expense_ratio = (self.monthly_expenses / self.monthly_income) * 100
        
        # Score calculation (lower expense = higher score)
        if expense_ratio <= 50:
            score = 100
        elif expense_ratio <= 60:
            score = 80
        elif expense_ratio <= 70:
            score = 60
        elif expense_ratio <= 80:
            score = 40
        else:
            score = 20
        
        status, emoji = self._get_status(score)
        
        if expense_ratio <= 50:
            suggestion = "Great expense management! Continue tracking"
        else:
            suggestion = f"Reduce expenses to ₹{self.monthly_income * 0.5:,.0f} (50% of income)"
        
        return HealthMetric(
            category=HealthCategory.EXPENSE_RATIO.value,
            score=score,
            weight=self.WEIGHTS[HealthCategory.EXPENSE_RATIO],
            status=status,
            message=f"Expense ratio: {expense_ratio:.1f}% of income",
            suggestion=suggestion
        )
    
    def calculate_overall_score(self) -> HealthReport:
        """
        Calculate overall financial health score and generate report
        
        Returns:
            HealthReport with all metrics and recommendations
        """
        metrics = [
            self.calculate_emergency_fund_score(),
            self.calculate_debt_ratio_score(),
            self.calculate_savings_rate_score(),
            self.calculate_investment_ratio_score(),
            self.calculate_insurance_score(),
            self.calculate_retirement_score(),
            self.calculate_credit_score_metric(),
            self.calculate_expense_ratio_score()
        ]
        
        # Weighted average
        overall_score = sum(m.score * m.weight for m in metrics)
        
        # Grade calculation
        if overall_score >= 90:
            grade = 'A+'
        elif overall_score >= 80:
            grade = 'A'
        elif overall_score >= 70:
            grade = 'B'
        elif overall_score >= 60:
            grade = 'C'
        elif overall_score >= 50:
            grade = 'D'
        else:
            grade = 'F'
        
        # Strengths and weaknesses
        strengths = [m.message for m in metrics if m.status in ['excellent', 'good']]
        weaknesses = [m.message for m in metrics if m.status in ['poor', 'critical']]
        
        # Recommendations
        recommendations = [m.suggestion for m in metrics if m.score < 70]
        
        # Monthly surplus
        monthly_surplus = self.monthly_income - self.monthly_expenses - self.monthly_emi - self.monthly_savings - self.monthly_investments
        
        # Financial age (based on habits, not actual age)
        financial_age = self.age
        if overall_score >= 80:
            financial_age += 10  # Ahead of peers
        elif overall_score >= 60:
            financial_age += 5
        elif overall_score < 40:
            financial_age -= 5  # Behind peers
        
        return HealthReport(
            overall_score=round(overall_score, 1),
            grade=grade,
            metrics=metrics,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            monthly_surplus=monthly_surplus,
            financial_age=max(18, financial_age)
        )


def get_health_score(
    monthly_income: float,
    monthly_expenses: float,
    **kwargs
) -> Dict:
    """
    Convenience function to get health score
    
    Args:
        monthly_income: Gross monthly income
        monthly_expenses: Monthly expenses
        **kwargs: Other parameters
        
    Returns:
        Dictionary with health report
    """
    calculator = FinancialHealthCalculator(
        monthly_income=monthly_income,
        monthly_expenses=monthly_expenses,
        **kwargs
    )
    
    report = calculator.calculate_overall_score()
    
    return {
        'overall_score': report.overall_score,
        'grade': report.grade,
        'financial_age': report.financial_age,
        'monthly_surplus': report.monthly_surplus,
        'metrics': [
            {
                'category': m.category,
                'score': m.score,
                'weight': m.weight,
                'status': m.status,
                'message': m.message,
                'suggestion': m.suggestion
            }
            for m in report.metrics
        ],
        'strengths': report.strengths,
        'weaknesses': report.weaknesses,
        'recommendations': report.recommendations
    }
