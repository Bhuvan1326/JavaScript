"""
KarVid Agent - Tax Brackets Module
Indian Income Tax Slabs for FY 2025-26 (AY 2026-27)

This module contains the income tax slabs for both New and Old tax regimes.
Data sourced from Budget 2025 announcements.
"""

from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TaxSlab:
    """Represents a single tax slab"""
    lower: float  # Lower limit in rupees
    upper: float  # Upper limit in rupees (None for unlimited)
    rate: float    # Tax rate as percentage
    
    def __str__(self):
        upper_str = f"₹{self.upper/100000:.0f}L" if self.upper else "Above"
        lower_str = f"₹{self.lower/100000:.0f}L" if self.lower else "₹0"
        return f"{lower_str} - {upper_str}: {self.rate}%"


# ============================================================
# NEW TAX REGIME - FY 2025-26 (Default Regime)
# ============================================================
# Budget 2025 introduced new slabs with zero-tax threshold at ₹12L
# Standard deduction: ₹75,000 for salaried individuals
# Section 87A rebate: Up to ₹60,000 (makes income up to ₹12L tax-free)

NEW_REGIME_SLABS_FY2025_26: List[TaxSlab] = [
    TaxSlab(lower=0, upper=400000, rate=0),       # ₹0 - ₹4L: NIL
    TaxSlab(lower=400000, upper=800000, rate=5),   # ₹4L - ₹8L: 5%
    TaxSlab(lower=800000, upper=1200000, rate=10), # ₹8L - ₹12L: 10%
    TaxSlab(lower=1200000, upper=1600000, rate=15),# ₹12L - ₹16L: 15%
    TaxSlab(lower=1600000, upper=2000000, rate=20),# ₹16L - ₹20L: 20%
    TaxSlab(lower=2000000, upper=2400000, rate=25),# ₹20L - ₹24L: 25%
    TaxSlab(lower=2400000, upper=None, rate=30),  # Above ₹24L: 30%
]

# New Regime Benefits
NEW_REGIME_STANDARD_DEDUCTION = 75000  # ₹75,000 for salaried
NEW_REGIME_REBATE_LIMIT = 1200000      # Income up to ₹12L is tax-free
NEW_REGIME_REBATE_MAX = 60000          # Max rebate under 87A


# ============================================================
# OLD TAX REGIME - FY 2025-26
# ============================================================
# Traditional slabs with deductions and exemptions
# Section 87A rebate: Up to ₹12,500 (income up to ₹5L)

OLD_REGIME_SLABS_FY2025_26: List[TaxSlab] = [
    TaxSlab(lower=0, upper=250000, rate=0),       # ₹0 - ₹2.5L: NIL
    TaxSlab(lower=250000, upper=500000, rate=5),   # ₹2.5L - ₹5L: 5%
    TaxSlab(lower=500000, upper=1000000, rate=20), # ₹5L - ₹10L: 20%
    TaxSlab(lower=1000000, upper=None, rate=30),  # Above ₹10L: 30%
]

# Old Regime Benefits
OLD_REGIME_STANDARD_DEDUCTION = 50000   # ₹50,000 for salaried
OLD_REGIME_REBATE_LIMIT = 500000        # Income up to ₹5L gets rebate
OLD_REGIME_REBATE_MAX = 12500          # Max rebate under 87A


def calculate_tax_by_slabs(taxable_income: float, slabs: List[TaxSlab]) -> float:
    """
    Calculate tax based on progressive slabs.
    
    Args:
        taxable_income: Taxable income in rupees
        slabs: List of TaxSlab objects
        
    Returns:
        Total tax amount in rupees
    """
    total_tax = 0.0
    
    for slab in slabs:
        if taxable_income <= slab.lower:
            break
            
        upper = slab.upper if slab.upper else taxable_income
        taxable_in_slab = min(taxable_income, upper) - slab.lower
        
        if taxable_in_slab > 0:
            tax_in_slab = (taxable_in_slab * slab.rate) / 100
            total_tax += tax_in_slab
    
    return total_tax


def calculate_new_regime_tax(income: float, is_salaried: bool = True, age: int = None) -> dict:
    """
    Calculate tax under New Tax Regime for FY 2025-26.
    
    Args:
        income: Gross income in rupees
        is_salaried: Whether the individual is a salaried employee
        age: Age of the taxpayer (not applicable for new regime)
        
    Returns:
        Dictionary with tax breakdown
    """
    # Apply standard deduction for salaried
    standard_deduction = NEW_REGIME_STANDARD_DEDUCTION if is_salaried else 0
    taxable_income = max(0, income - standard_deduction)
    
    # Calculate base tax
    base_tax = calculate_tax_by_slabs(taxable_income, NEW_REGIME_SLABS_FY2025_26)
    
    # Apply Section 87A rebate
    rebate = 0
    if taxable_income <= NEW_REGIME_REBATE_LIMIT:
        rebate = min(base_tax, NEW_REGIME_REBATE_MAX)
    
    # Apply Health & Education Cess (4%)
    tax_after_rebate = base_tax - rebate
    cess = tax_after_rebate * 0.04
    total_tax = tax_after_rebate + cess
    
    return {
        "gross_income": income,
        "standard_deduction": standard_deduction,
        "taxable_income": taxable_income,
        "base_tax": round(base_tax, 2),
        "section_87a_rebate": round(rebate, 2),
        "tax_after_rebate": round(tax_after_rebate, 2),
        "cess_4_percent": round(cess, 2),
        "total_tax": round(total_tax, 2),
        "effective_rate": round((total_tax / income * 100) if income > 0 else 0, 2)
    }


def calculate_old_regime_tax(income: float, is_salaried: bool = True, 
                             deductions: float = 0, age: int = None) -> dict:
    """
    Calculate tax under Old Tax Regime for FY 2025-26.
    
    Args:
        income: Gross income in rupees
        is_salaried: Whether the individual is a salaried employee
        deductions: Total deductions claimed (80C, 80D, HRA, etc.)
        age: Age of the taxpayer (affects rebate limits)
        
    Returns:
        Dictionary with tax breakdown
    """
    # Apply standard deduction for salaried
    standard_deduction = OLD_REGIME_STANDARD_DEDUCTION if is_salaried else 0
    taxable_income = max(0, income - standard_deduction - deductions)
    
    # Calculate base tax
    base_tax = calculate_tax_by_slabs(taxable_income, OLD_REGIME_SLABS_FY2025_26)
    
    # Apply Section 87A rebate
    rebate = 0
    if taxable_income <= OLD_REGIME_REBATE_LIMIT:
        rebate = min(base_tax, OLD_REGIME_REBATE_MAX)
    
    # Apply Health & Education Cess (4%)
    tax_after_rebate = base_tax - rebate
    cess = tax_after_rebate * 0.04
    total_tax = tax_after_rebate + cess
    
    return {
        "gross_income": income,
        "standard_deduction": standard_deduction,
        "other_deductions": deductions,
        "taxable_income": taxable_income,
        "base_tax": round(base_tax, 2),
        "section_87a_rebate": round(rebate, 2),
        "tax_after_rebate": round(tax_after_rebate, 2),
        "cess_4_percent": round(cess, 2),
        "total_tax": round(total_tax, 2),
        "effective_rate": round((total_tax / income * 100) if income > 0 else 0, 2)
    }


def compare_regimes(income: float, is_salaried: bool = True, 
                    old_regime_deductions: float = 0) -> dict:
    """
    Compare tax liability under both regimes.
    
    Args:
        income: Gross income in rupees
        is_salaried: Whether salaried employee
        old_regime_deductions: Total deductions for old regime
        
    Returns:
        Comparison dictionary with recommendation
    """
    new_tax = calculate_new_regime_tax(income, is_salaried)
    old_tax = calculate_old_regime_tax(income, is_salaried, old_regime_deductions)
    
    savings = old_tax["total_tax"] - new_tax["total_tax"]
    
    return {
        "income": income,
        "new_regime": new_tax,
        "old_regime": old_tax,
        "difference": round(savings, 2),
        "recommended_regime": "NEW" if savings > 0 else "OLD",
        "savings_with_recommended": abs(round(savings, 2))
    }


# ============================================================
# SURCHARGE RATES (Above ₹50L taxable income)
# ============================================================
SURCHARGE_RATES = {
    (5000000, 10000000): 0.10,   # ₹50L - ₹1Cr: 10%
    (10000000, 20000000): 0.15,  # ₹1Cr - ₹2Cr: 15%
    (20000000, 50000000): 0.25,  # ₹2Cr - ₹5Cr: 25%
    (50000000, float('inf')): 0.37,  # Above ₹5Cr: 37%
}

# Marginal Relief: Surcharge capped to limit effective rate
# For income > ₹5Cr, max surcharge is 37% (not applicable on capital gains)


def calculate_surcharge(taxable_income: float, base_tax: float) -> float:
    """
    Calculate surcharge based on taxable income.
    
    Args:
        taxable_income: Taxable income in rupees
        base_tax: Base tax amount
        
    Returns:
        Surcharge amount
    """
    for (lower, upper), rate in SURCHARGE_RATES.items():
        if lower < taxable_income <= upper:
            return base_tax * rate
    return 0.0


# ============================================================
# EXAMPLE USAGE
# ============================================================
if __name__ == "__main__":
    # Example: Compare both regimes for ₹15L income
    income = 1500000
    
    print("="*60)
    print(f"TAX COMPARISON FOR ₹{income/100000:.0f}L INCOME (FY 2025-26)")
    print("="*60)
    
    # New Regime
    new_result = calculate_new_regime_tax(income, is_salaried=True)
    print("\n📊 NEW TAX REGIME:")
    print(f"   Taxable Income: ₹{new_result['taxable_income']:,.0f}")
    print(f"   Base Tax: ₹{new_result['base_tax']:,.0f}")
    print(f"   87A Rebate: ₹{new_result['section_87a_rebate']:,.0f}")
    print(f"   Cess (4%): ₹{new_result['cess_4_percent']:,.0f}")
    print(f"   TOTAL TAX: ₹{new_result['total_tax']:,.0f}")
    print(f"   Effective Rate: {new_result['effective_rate']}%")
    
    # Old Regime (with ₹1.5L deductions)
    old_result = calculate_old_regime_tax(income, is_salaried=True, deductions=150000)
    print("\n📊 OLD TAX REGIME (with ₹1.5L deductions):")
    print(f"   Taxable Income: ₹{old_result['taxable_income']:,.0f}")
    print(f"   Base Tax: ₹{old_result['base_tax']:,.0f}")
    print(f"   87A Rebate: ₹{old_result['section_87a_rebate']:,.0f}")
    print(f"   Cess (4%): ₹{old_result['cess_4_percent']:,.0f}")
    print(f"   TOTAL TAX: ₹{old_result['total_tax']:,.0f}")
    print(f"   Effective Rate: {old_result['effective_rate']}%")
    
    # Comparison
    comparison = compare_regimes(income, is_salaried=True, old_regime_deductions=150000)
    print("\n" + "="*60)
    print(f"💡 RECOMMENDATION: {comparison['recommended_regime']} REGIME")
    print(f"   Savings: ₹{comparison['savings_with_recommended']:,.0f}")
    print("="*60)
