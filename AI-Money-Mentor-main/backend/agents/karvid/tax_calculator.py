"""
KarVid Agent - Main Tax Calculator
Comprehensive Indian Tax Calculator for FY 2025-26

This module integrates:
- Income Tax Slabs (New & Old Regime)
- Deductions (80C, 80D, HRA, etc.)
- Capital Gains Tax
- Tax Optimization Strategies

Author: KarVid Agent - AI Money Mentor
Version: 1.0.0
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import json

# Import local modules
from agents.karvid.tax_brackets import (
    calculate_new_regime_tax,
    calculate_old_regime_tax,
    compare_regimes,
    NEW_REGIME_SLABS_FY2025_26,
    OLD_REGIME_SLABS_FY2025_26,
)
from agents.karvid.deductions import (
    calculate_80c_deduction,
    calculate_80d_deduction,
    calculate_hra_exemption,
    calculate_80ccd_deduction,
    calculate_total_deductions,
)
from agents.karvid.capital_gains import (
    calculate_capital_gains,
    calculate_section_54_exemption,
    CapitalGainsResult,
)


# ============================================================
# TAX CALCULATOR CLASS
# ============================================================

@dataclass
class TaxpayerProfile:
    """Taxpayer information for tax calculation"""
    name: str = ""
    age: int = 30
    is_senior_citizen: bool = False
    is_salaried: bool = True
    pan: str = ""
    
    # Income sources
    salary_income: float = 0
    business_income: float = 0
    rental_income: float = 0
    other_income: float = 0
    capital_gains_stcg: float = 0
    capital_gains_ltcg: float = 0
    
    # Deductions
    ppf: float = 0
    epf: float = 0
    elss: float = 0
    life_insurance: float = 0
    home_loan_principal: float = 0
    home_loan_interest: float = 0
    tuition_fees: float = 0
    health_insurance_self: float = 0
    health_insurance_parents: float = 0
    nps_contribution: float = 0
    hra_received: float = 0
    rent_paid: float = 0
    basic_salary: float = 0
    metro_city: bool = False
    
    # Parents info
    parents_age: int = 0


@dataclass
class TaxCalculationResult:
    """Complete tax calculation result"""
    gross_income: float
    deductions: float
    taxable_income: float
    base_tax: float
    rebate: float
    cess: float
    total_tax: float
    effective_rate: float
    regime: str
    breakdown: Dict[str, Any]


class KarVidTaxCalculator:
    """
    Main Tax Calculator for Indian Income Tax FY 2025-26.
    
    Features:
    - Compare New vs Old Tax Regime
    - Calculate all deductions
    - Calculate capital gains tax
    - Generate optimization recommendations
    """
    
    def __init__(self, profile: TaxpayerProfile = None):
        """
        Initialize tax calculator.
        
        Args:
            profile: TaxpayerProfile with income and deduction details
        """
        self.profile = profile or TaxpayerProfile()
        self.results = {}
    
    def calculate_gross_income(self) -> float:
        """Calculate total gross income from all sources."""
        return (
            self.profile.salary_income +
            self.profile.business_income +
            self.profile.rental_income +
            self.profile.other_income +
            self.profile.capital_gains_stcg +
            self.profile.capital_gains_ltcg
        )
    
    def calculate_deductions_old_regime(self) -> Dict[str, Any]:
        """Calculate all deductions available under Old Tax Regime."""
        # Section 80C
        deduction_80c = calculate_80c_deduction(
            ppf=self.profile.ppf,
            epf=self.profile.epf,
            elss=self.profile.elss,
            life_insurance_premium=self.profile.life_insurance,
            home_loan_principal=self.profile.home_loan_principal,
            tuition_fees=self.profile.tuition_fees,
        )
        
        # Section 80D
        deduction_80d = calculate_80d_deduction(
            self_health_insurance=self.profile.health_insurance_self,
            parents_health_insurance=self.profile.health_insurance_parents,
            self_age=self.profile.age,
            parents_age=self.profile.parents_age,
        )
        
        # HRA Exemption
        hra_result = None
        if self.profile.hra_received > 0:
            hra_result = calculate_hra_exemption(
                hra_received=self.profile.hra_received,
                basic_salary=self.profile.basic_salary,
                rent_paid=self.profile.rent_paid,
                metro_city=self.profile.metro_city,
            )
        
        # NPS Additional (80CCD(1B))
        nps_additional = min(self.profile.nps_contribution, 50000)
        
        # Home Loan Interest (24(b))
        home_loan_interest_deduction = min(self.profile.home_loan_interest, 200000)
        
        # Total deductions
        total_80c = deduction_80c['allowed_deduction']
        total_80d = deduction_80d['total_deduction']
        hra_exempt = hra_result['hra_exemption'] if hra_result else 0
        
        total_deductions = (
            50000 +  # Standard deduction
            total_80c +
            total_80d +
            hra_exempt +
            nps_additional +
            home_loan_interest_deduction
        )
        
        return {
            "standard_deduction": 50000,
            "section_80c": deduction_80c,
            "section_80d": deduction_80d,
            "hra_exemption": hra_result,
            "nps_additional_80ccd1b": nps_additional,
            "home_loan_interest_24b": home_loan_interest_deduction,
            "total_deductions": total_deductions,
        }
    
    def calculate_deductions_new_regime(self) -> Dict[str, Any]:
        """Calculate deductions available under New Tax Regime."""
        # New regime has limited deductions
        # Standard deduction: ₹75,000
        # Employer NPS contribution (80CCD(2)): Available
        
        return {
            "standard_deduction": 75000,
            "employer_nps_80ccd2": 0,  # To be filled by employer
            "total_deductions": 75000,
            "note": "Most deductions not available in New Regime"
        }
    
    def calculate_income_tax(
        self,
        regime: str = "new",
        custom_deductions: float = None
    ) -> TaxCalculationResult:
        """
        Calculate income tax for the given regime.
        
        Args:
            regime: 'new' or 'old'
            custom_deductions: Override automatic deduction calculation
            
        Returns:
            TaxCalculationResult with complete breakdown
        """
        gross_income = self.calculate_gross_income()
        
        if regime.lower() == "new":
            # New Tax Regime
            result = calculate_new_regime_tax(
                income=gross_income,
                is_salaried=self.profile.is_salaried,
                age=self.profile.age,
            )
            regime_name = "NEW"
            
        else:
            # Old Tax Regime
            if custom_deductions is None:
                deductions_data = self.calculate_deductions_old_regime()
                deductions = deductions_data['total_deductions']
            else:
                deductions = custom_deductions
            
            result = calculate_old_regime_tax(
                income=gross_income,
                is_salaried=self.profile.is_salaried,
                deductions=deductions,
                age=self.profile.age,
            )
            regime_name = "OLD"
        
        return TaxCalculationResult(
            gross_income=gross_income,
            deductions=result.get('standard_deduction', 0) + result.get('other_deductions', 0),
            taxable_income=result['taxable_income'],
            base_tax=result['base_tax'],
            rebate=result['section_87a_rebate'],
            cess=result['cess_4_percent'],
            total_tax=result['total_tax'],
            effective_rate=result['effective_rate'],
            regime=regime_name,
            breakdown=result,
        )
    
    def compare_tax_regimes(self) -> Dict[str, Any]:
        """
        Compare tax liability under both regimes.
        
        Returns:
            Dictionary with comparison and recommendation
        """
        new_tax = self.calculate_income_tax(regime="new")
        old_tax = self.calculate_income_tax(regime="old")
        
        savings = old_tax.total_tax - new_tax.total_tax
        
        return {
            "gross_income": self.calculate_gross_income(),
            "new_regime": {
                "total_deductions": new_tax.deductions,
                "taxable_income": new_tax.taxable_income,
                "total_tax": new_tax.total_tax,
                "effective_rate": new_tax.effective_rate,
            },
            "old_regime": {
                "total_deductions": old_tax.deductions,
                "taxable_income": old_tax.taxable_income,
                "total_tax": old_tax.total_tax,
                "effective_rate": old_tax.effective_rate,
            },
            "difference": abs(savings),
            "recommended_regime": "NEW" if savings > 0 else "OLD",
            "savings_with_recommended": abs(savings),
            "break_even_deductions": self._calculate_break_even_deductions(),
        }
    
    def _calculate_break_even_deductions(self) -> float:
        """
        Calculate minimum deductions needed for Old Regime to be beneficial.
        
        Returns:
            Break-even deduction amount
        """
        # For each income level, find the deduction needed
        # where Old Regime tax = New Regime tax
        gross_income = self.calculate_gross_income()
        
        # Rough estimate: deductions needed to match new regime tax
        # This varies by income level
        new_tax = self.calculate_income_tax(regime="new")
        
        # Binary search for break-even point
        low, high = 0, 500000  # Max reasonable deductions
        target_tax = new_tax.total_tax
        
        for _ in range(20):  # Binary search iterations
            mid = (low + high) / 2
            old_tax = self.calculate_income_tax(regime="old", custom_deductions=mid)
            
            if old_tax.total_tax < target_tax:
                high = mid
            else:
                low = mid
        
        return round(mid, 0)
    
    def calculate_capital_gains_tax(
        self,
        asset_type: str,
        sale_price: float,
        purchase_price: float,
        purchase_date: datetime,
        sale_date: datetime = None,
        **kwargs
    ) -> CapitalGainsResult:
        """
        Calculate capital gains tax for a specific transaction.
        
        Args:
            asset_type: 'equity', 'equity_mf', 'debt_mf', 'real_estate', 'unlisted_shares'
            sale_price: Sale consideration
            purchase_price: Purchase cost
            purchase_date: Date of purchase
            sale_date: Date of sale (defaults to today)
            **kwargs: Additional parameters
            
        Returns:
            CapitalGainsResult object
        """
        sale_dt = sale_date or datetime.now()
        days_held = (sale_dt - purchase_date).days
        
        return calculate_capital_gains(
            asset_type=asset_type,
            sale_price=sale_price,
            purchase_price=purchase_price,
            days_held=days_held,
            purchase_date=purchase_date,
            **kwargs
        )
    
    def generate_tax_saving_recommendations(self) -> List[Dict[str, Any]]:
        """
        Generate personalized tax saving recommendations.
        
        Returns:
            List of recommendations with potential savings
        """
        recommendations = []
        
        # Check 80C utilization
        deduction_80c = calculate_80c_deduction(
            ppf=self.profile.ppf,
            epf=self.profile.epf,
            elss=self.profile.elss,
            life_insurance_premium=self.profile.life_insurance,
            home_loan_principal=self.profile.home_loan_principal,
        )
        
        if deduction_80c['unused_limit'] > 0:
            recommendations.append({
                "category": "Section 80C",
                "type": "UNDER_UTILIZED",
                "message": f"You have ₹{deduction_80c['unused_limit']:,} unused 80C limit",
                "potential_savings": deduction_80c['unused_limit'] * 0.30,  # At 30% slab
                "actions": [
                    "Invest in PPF (up to ₹1.5L)",
                    "Invest in ELSS mutual funds (3-year lock-in)",
                    "Contribute to NPS Tier-1",
                    "Pay life insurance premium",
                    "Repay home loan principal",
                ]
            })
        
        # Check 80D utilization
        deduction_80d = calculate_80d_deduction(
            self_health_insurance=self.profile.health_insurance_self,
            parents_health_insurance=self.profile.health_insurance_parents,
            self_age=self.profile.age,
            parents_age=self.profile.parents_age,
        )
        
        max_80d = 100000 if self.profile.age >= 60 else 75000
        used_80d = deduction_80d['total_deduction']
        
        if used_80d < max_80d:
            unused_80d = max_80d - used_80d
            recommendations.append({
                "category": "Section 80D",
                "type": "UNDER_UTILIZED",
                "message": f"You can claim up to ₹{unused_80d:,} more under 80D",
                "potential_savings": unused_80d * 0.30,
                "actions": [
                    "Buy health insurance for self/family",
                    "Buy health insurance for parents",
                    "Claim preventive health check-up expenses",
                ]
            })
        
        # Check NPS additional deduction
        if self.profile.nps_contribution < 50000:
            unused_nps = 50000 - self.profile.nps_contribution
            recommendations.append({
                "category": "NPS (80CCD(1B))",
                "type": "ADDITIONAL_DEDUCTION",
                "message": f"Additional ₹{unused_nps:,} can be invested in NPS for extra deduction",
                "potential_savings": unused_nps * 0.30,
                "actions": [
                    "Invest in NPS Tier-1 account",
                    "Maximum deduction: ₹50,000 (beyond 80C)",
                    "Only available in Old Tax Regime",
                ]
            })
        
        # Regime recommendation
        comparison = self.compare_tax_regimes()
        if comparison['recommended_regime'] == 'OLD':
            recommendations.append({
                "category": "Tax Regime",
                "type": "REGIME_RECOMMENDATION",
                "message": "Old Tax Regime may save you more tax",
                "potential_savings": comparison['savings_with_recommended'],
                "actions": [
                    "Opt for Old Tax Regime while filing ITR",
                    "Ensure you claim all eligible deductions",
                    f"Break-even deductions: ₹{comparison['break_even_deductions']:,}",
                ]
            })
        else:
            recommendations.append({
                "category": "Tax Regime",
                "type": "REGIME_RECOMMENDATION",
                "message": "New Tax Regime is better for your profile",
                "potential_savings": comparison['savings_with_recommended'],
                "actions": [
                    "New Regime offers lower tax rates",
                    "No need to invest in tax-saving instruments",
                    "Simple filing with minimal documentation",
                ]
            })
        
        return recommendations
    
    def generate_tax_report(self) -> str:
        """
        Generate a comprehensive tax report.
        
        Returns:
            Formatted tax report as string
        """
        gross_income = self.calculate_gross_income()
        comparison = self.compare_tax_regimes()
        recommendations = self.generate_tax_saving_recommendations()
        
        report = f"""
{'='*70}
KARVID TAX REPORT - FY 2025-26 (AY 2026-27)
{'='*70}

TAXPAYER PROFILE:
-----------------
Name: {self.profile.name or 'Not Provided'}
Age: {self.profile.age} years
Employment: {'Salaried' if self.profile.is_salaried else 'Self-Employed/Business'}

INCOME SUMMARY:
---------------
Gross Total Income: ₹{gross_income:,.0f}
  - Salary Income: ₹{self.profile.salary_income:,.0f}
  - Business Income: ₹{self.profile.business_income:,.0f}
  - Rental Income: ₹{self.profile.rental_income:,.0f}
  - Other Income: ₹{self.profile.other_income:,.0f}
  - STCG: ₹{self.profile.capital_gains_stcg:,.0f}
  - LTCG: ₹{self.profile.capital_gains_ltcg:,.0f}

TAX COMPARISON:
---------------
{'NEW REGIME':<20} {'OLD REGIME':<20}
{'-'*40}
Deductions: ₹{comparison['new_regime']['total_deductions']:>15,.0f} ₹{comparison['old_regime']['total_deductions']:>15,.0f}
Taxable Income: ₹{comparison['new_regime']['taxable_income']:>13,.0f} ₹{comparison['old_regime']['taxable_income']:>13,.0f}
Tax Payable: ₹{comparison['new_regime']['total_tax']:>17,.0f} ₹{comparison['old_regime']['total_tax']:>17,.0f}
Effective Rate: {comparison['new_regime']['effective_rate']:>14.2f}% {comparison['old_regime']['effective_rate']:>14.2f}%

RECOMMENDATION: {comparison['recommended_regime']} REGIME
Potential Savings: ₹{comparison['savings_with_recommended']:,.0f}

TAX SAVING RECOMMENDATIONS:
---------------------------
"""
        
        for i, rec in enumerate(recommendations, 1):
            report += f"""
{i}. {rec['category']} - {rec['type']}
   {rec['message']}
   Potential Savings: ₹{rec['potential_savings']:,.0f}
   Actions:
"""
            for action in rec['actions']:
                report += f"   - {action}\n"
        
        report += f"""
DISCLAIMER:
-----------
This is an estimate based on current FY 2025-26 tax rules.
Actual tax liability may vary based on specific circumstances.
Consult a tax professional for personalized advice.

Generated by: KarVid Agent - AI Money Mentor
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""
        
        return report


# ============================================================
# QUICK CALCULATION FUNCTIONS
# ============================================================

def quick_tax_estimate(
    income: float,
    is_salaried: bool = True,
    regime: str = "new",
    deductions: float = 0
) -> Dict[str, float]:
    """
    Quick tax estimate without full profile.
    
    Args:
        income: Gross income
        is_salaried: Whether salaried
        regime: 'new' or 'old'
        deductions: Total deductions (for old regime)
        
    Returns:
        Dictionary with key tax figures
    """
    profile = TaxpayerProfile(
        is_salaried=is_salaried,
        salary_income=income,
    )
    calculator = KarVidTaxCalculator(profile)
    
    if regime.lower() == "new":
        result = calculator.calculate_income_tax(regime="new")
    else:
        result = calculator.calculate_income_tax(regime="old", custom_deductions=deductions)
    
    return {
        "gross_income": result.gross_income,
        "taxable_income": result.taxable_income,
        "total_tax": result.total_tax,
        "effective_rate": result.effective_rate,
    }


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":
    # Create a sample taxpayer profile
    profile = TaxpayerProfile(
        name="Sample Taxpayer",
        age=32,
        is_senior_citizen=False,
        is_salaried=True,
        salary_income=1500000,
        rental_income=200000,
        other_income=50000,
        ppf=100000,
        epf=36000,
        elss=50000,
        life_insurance=25000,
        home_loan_principal=80000,
        home_loan_interest=180000,
        health_insurance_self=20000,
        health_insurance_parents=30000,
        parents_age=65,
        nps_contribution=50000,
        hra_received=120000,
        rent_paid=180000,
        basic_salary=600000,
        metro_city=True,
    )
    
    # Initialize calculator
    calculator = KarVidTaxCalculator(profile)
    
    # Generate comprehensive report
    print(calculator.generate_tax_report())
    
    # Quick comparison
    print("\n" + "="*70)
    print("QUICK REGIME COMPARISON")
    print("="*70)
    
    comparison = calculator.compare_tax_regimes()
    print(f"\nNew Regime Tax: ₹{comparison['new_regime']['total_tax']:,.0f}")
    print(f"Old Regime Tax: ₹{comparison['old_regime']['total_tax']:,.0f}")
    print(f"\nRecommended: {comparison['recommended_regime']} REGIME")
    print(f"Savings: ₹{comparison['savings_with_recommended']:,.0f}")
    
    # Generate recommendations
    print("\n" + "="*70)
    print("TAX SAVING RECOMMENDATIONS")
    print("="*70)
    
    recommendations = calculator.generate_tax_saving_recommendations()
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['category']}: {rec['message']}")
        print(f"   Potential Savings: ₹{rec['potential_savings']:,.0f}")
