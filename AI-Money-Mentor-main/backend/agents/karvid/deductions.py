"""
KarVid Agent - Deductions Module
Indian Income Tax Deductions for FY 2025-26

This module contains calculations for:
- Section 80C (Investments & Expenses) - Max ₹1,50,000
- Section 80D (Health Insurance) - Max ₹1,00,000
- HRA (House Rent Allowance) Exemption
- Other key deductions (80E, 80EE, 80CCD, etc.)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


# ============================================================
# SECTION 80C - INVESTMENTS & EXPENSES (Max ₹1,50,000)
# ============================================================

@dataclass
class Deduction80C:
    """Represents a single 80C deduction item"""
    name: str
    max_limit: float
    description: str
    category: str  # 'investment', 'expense', 'insurance'


# List of all 80C eligible deductions
DEDUCTIONS_80C: List[Deduction80C] = [
    # Investments
    Deduction80C("PPF", 150000, "Public Provident Fund contributions", "investment"),
    Deduction80C("EPF", 150000, "Employee Provident Fund contributions", "investment"),
    Deduction80C("ELSS", 150000, "Equity Linked Savings Scheme (3-year lock-in)", "investment"),
    Deduction80C("NSC", 150000, "National Savings Certificate (5-year)", "investment"),
    Deduction80C("SSY", 150000, "Sukanya Samriddhi Yojana (girl child)", "investment"),
    Deduction80C("SCSS", 150000, "Senior Citizens Savings Scheme", "investment"),
    Deduction80C("Tax_Saving_FD", 150000, "Tax Saving Fixed Deposits (5-year)", "investment"),
    Deduction80C("NPS_80C", 150000, "NPS Tier-1 contributions", "investment"),
    Deduction80C("ULIP", 150000, "Unit Linked Insurance Plans", "investment"),
    
    # Insurance Premium
    Deduction80C("Life_Insurance", 150000, "Life insurance premium (self/spouse/children)", "insurance"),
    
    # Expenses
    Deduction80C("Home_Loan_Principal", 150000, "Home loan principal repayment", "expense"),
    Deduction80C("Tuition_Fees", 150000, "Children's tuition fees (max 2 children)", "expense"),
    Deduction80C("Stamp_Duty", 150000, "Stamp duty/registration for house purchase", "expense"),
]

# 80C Overall Limit
SECTION_80C_LIMIT = 150000  # ₹1,50,000


def calculate_80c_deduction(
    ppf: float = 0,
    epf: float = 0,
    elss: float = 0,
    nsc: float = 0,
    ssy: float = 0,
    scss: float = 0,
    tax_saving_fd: float = 0,
    nps_tier1: float = 0,
    life_insurance_premium: float = 0,
    home_loan_principal: float = 0,
    tuition_fees: float = 0,
    stamp_duty: float = 0,
    ulip: float = 0,
    other_investments: float = 0
) -> dict:
    """
    Calculate total 80C deduction with breakdown.
    
    Returns:
        Dictionary with total deduction, breakdown, and unused limit
    """
    investments = {
        "ppf": ppf,
        "epf": epf,
        "elss": elss,
        "nsc": nsc,
        "ssy": ssy,
        "scss": scss,
        "tax_saving_fd": tax_saving_fd,
        "nps_tier1": nps_tier1,
        "ulip": ulip,
        "other_investments": other_investments,
    }
    
    expenses = {
        "life_insurance_premium": life_insurance_premium,
        "home_loan_principal": home_loan_principal,
        "tuition_fees": tuition_fees,
        "stamp_duty": stamp_duty,
    }
    
    total_claimed = (
        ppf + epf + elss + nsc + ssy + scss + tax_saving_fd + 
        nps_tier1 + ulip + other_investments +
        life_insurance_premium + home_loan_principal + 
        tuition_fees + stamp_duty
    )
    
    allowed_deduction = min(total_claimed, SECTION_80C_LIMIT)
    unused_limit = max(0, SECTION_80C_LIMIT - allowed_deduction)
    
    return {
        "investments": investments,
        "expenses": expenses,
        "total_claimed": total_claimed,
        "allowed_deduction": allowed_deduction,
        "unused_limit": unused_limit,
        "limit": SECTION_80C_LIMIT,
    }


# ============================================================
# SECTION 80D - HEALTH INSURANCE (Max ₹1,00,000)
# ============================================================

@dataclass
class Deduction80D:
    """Represents 80D deduction categories"""
    name: str
    max_limit: float
    description: str


# 80D Limits
SECTION_80D_SELF_LIMIT = 25000          # Self/family (below 60 years)
SECTION_80D_SELF_SENIOR_LIMIT = 50000   # Self/family (60+ years)
SECTION_80D_PARENTS_LIMIT = 25000       # Parents (below 60 years)
SECTION_80D_PARENTS_SENIOR_LIMIT = 50000 # Parents (60+ years)
SECTION_80D_PREVENTIVE_CHECKUP = 5000   # Preventive health check-up (within overall)


def calculate_80d_deduction(
    self_health_insurance: float = 0,
    parents_health_insurance: float = 0,
    self_age: int = None,
    parents_age: int = None,
    preventive_checkup_expense: float = 0,
    self_is_senior: bool = False,
    parents_are_senior: bool = False
) -> dict:
    """
    Calculate Section 80D deduction for health insurance.
    
    Args:
        self_health_insurance: Premium for self/family
        parents_health_insurance: Premium for parents
        self_age: Age of taxpayer
        parents_age: Age of parents
        preventive_checkup_expense: Preventive health check-up cost
        self_is_senior: Whether taxpayer is senior citizen (60+)
        parents_are_senior: Whether parents are senior citizens (60+)
        
    Returns:
        Dictionary with deduction breakdown
    """
    # Determine limits based on age
    self_limit = SECTION_80D_SELF_SENIOR_LIMIT if (self_is_senior or (self_age and self_age >= 60)) else SECTION_80D_SELF_LIMIT
    parents_limit = SECTION_80D_PARENTS_SENIOR_LIMIT if (parents_are_senior or (parents_age and parents_age >= 60)) else SECTION_80D_PARENTS_LIMIT
    
    # Calculate allowed deductions
    self_deduction = min(self_health_insurance, self_limit)
    parents_deduction = min(parents_health_insurance, parents_limit)
    
    # Preventive check-up is part of the self limit
    preventive_deduction = min(preventive_checkup_expense, SECTION_80D_PREVENTIVE_CHECKUP)
    
    # Total deduction
    total_deduction = self_deduction + parents_deduction
    max_possible = self_limit + parents_limit
    
    return {
        "self_health_insurance": {
            "claimed": self_health_insurance,
            "allowed": self_deduction,
            "limit": self_limit,
        },
        "parents_health_insurance": {
            "claimed": parents_health_insurance,
            "allowed": parents_deduction,
            "limit": parents_limit,
        },
        "preventive_checkup": {
            "claimed": preventive_checkup_expense,
            "allowed": preventive_deduction,
            "limit": SECTION_80D_PREVENTIVE_CHECKUP,
        },
        "total_deduction": total_deduction,
        "maximum_possible": max_possible,
        "self_is_senior": self_is_senior or (self_age >= 60 if self_age else False),
        "parents_are_senior": parents_are_senior or (parents_age >= 60 if parents_age else False),
    }


# ============================================================
# HRA (HOUSE RENT ALLOWANCE) EXEMPTION
# ============================================================

def calculate_hra_exemption(
    hra_received: float,
    basic_salary: float,
    rent_paid: float,
    metro_city: bool = False,
    actual_rent_paid: float = None
) -> dict:
    """
    Calculate HRA exemption under Section 10(13A).
    
    The exemption is the MINIMUM of:
    1. Actual HRA received
    2. Rent paid - 10% of basic salary
    3. 40% of basic salary (non-metro) or 50% (metro city)
    
    Args:
        hra_received: HRA received from employer
        basic_salary: Basic salary (including DA if applicable)
        rent_paid: Total rent paid during the year
        metro_city: Whether living in metro city (Delhi, Mumbai, Chennai, Kolkata)
        actual_rent_paid: Actual rent paid (if different from rent_paid)
        
    Returns:
        Dictionary with HRA exemption calculation
    """
    rent = actual_rent_paid or rent_paid
    
    # Calculate the three values
    actual_hra = hra_received
    rent_minus_10_percent = max(0, rent - (basic_salary * 0.10))
    percentage_of_basic = basic_salary * (0.50 if metro_city else 0.40)
    
    # HRA exemption is minimum of the three
    hra_exemption = min(actual_hra, rent_minus_10_percent, percentage_of_basic)
    taxable_hra = max(0, hra_received - hra_exemption)
    
    return {
        "hra_received": hra_received,
        "basic_salary": basic_salary,
        "rent_paid": rent,
        "metro_city": metro_city,
        "calculation": {
            "actual_hra_received": actual_hra,
            "rent_minus_10pct_basic": rent_minus_10_percent,
            f"{'50%' if metro_city else '40%'}_of_basic": percentage_of_basic,
        },
        "hra_exemption": hra_exemption,
        "taxable_hra": taxable_hra,
        "notes": "HRA exemption is available only under Old Tax Regime"
    }


# ============================================================
# SECTION 80CCD - NPS CONTRIBUTIONS
# ============================================================

SECTION_80CCD1_LIMIT_SELF = 0.10  # 10% of salary (employed) or 20% of gross (self-employed)
SECTION_80CCD1B_ADDITIONAL = 50000  # Additional NPS deduction
SECTION_80CCD2_EMPLOYER = 0.10     # 10% of basic + DA (14% for Central Govt employees)


def calculate_80ccd_deduction(
    nps_contribution_self: float,
    nps_contribution_employer: float,
    salary: float = None,
    basic_da: float = None,
    gross_income: float = None,
    is_self_employed: bool = False,
    is_central_govt: bool = False
) -> dict:
    """
    Calculate NPS deductions under 80CCD.
    
    Args:
        nps_contribution_self: Employee's own NPS contribution
        nps_contribution_employer: Employer's NPS contribution
        salary: Total salary (for 80CCD(1) limit)
        basic_da: Basic + DA (for 80CCD(2) limit)
        gross_income: Gross income for self-employed
        is_self_employed: Whether taxpayer is self-employed
        is_central_govt: Whether taxpayer is Central Govt employee
        
    Returns:
        Dictionary with NPS deductions breakdown
    """
    # 80CCD(1) - Employee contribution (within overall 80CCE limit of 1.5L)
    if is_self_employed:
        limit_80ccd1 = (gross_income or 0) * 0.20  # 20% of gross income
    else:
        limit_80ccd1 = (salary or 0) * 0.10  # 10% of salary
    
    deduction_80ccd1 = min(nps_contribution_self, limit_80ccd1, 150000)
    
    # 80CCD(1B) - Additional ₹50,000 deduction (beyond 80C)
    deduction_80ccd1b = min(nps_contribution_self, SECTION_80CCD1B_ADDITIONAL)
    
    # 80CCD(2) - Employer contribution
    employer_rate = 0.14 if is_central_govt else 0.10
    limit_80ccd2 = (basic_da or salary or 0) * employer_rate
    deduction_80ccd2 = min(nps_contribution_employer, limit_80ccd2)
    
    return {
        "80ccd1_employee": {
            "contribution": nps_contribution_self,
            "allowed": deduction_80ccd1,
            "limit": min(limit_80ccd1, 150000),
        },
        "80ccd1b_additional": {
            "contribution": nps_contribution_self,
            "allowed": deduction_80ccd1b,
            "limit": SECTION_80CCD1B_ADDITIONAL,
        },
        "80ccd2_employer": {
            "contribution": nps_contribution_employer,
            "allowed": deduction_80ccd2,
            "limit": limit_80ccd2,
        },
        "total_nps_deduction": deduction_80ccd1 + deduction_80ccd1b + deduction_80ccd2,
        "note": "80CCD(1) is within overall 80CCE limit of ₹1.5L. 80CCD(1B) is additional."
    }


# ============================================================
# SECTION 80E - EDUCATION LOAN INTEREST
# ============================================================

def calculate_80e_deduction(
    education_loan_interest: float,
    years_remaining: int = None
) -> dict:
    """
    Calculate Section 80E deduction for education loan interest.
    
    Args:
        education_loan_interest: Interest paid on education loan
        years_remaining: Years remaining in the 8-year deduction period
        
    Returns:
        Dictionary with deduction details
    """
    # No limit on deduction amount, but limited to 8 years
    # Available for self, spouse, children, or student under legal guardianship
    
    return {
        "interest_paid": education_loan_interest,
        "deduction_allowed": education_loan_interest,  # No upper limit
        "deduction_period": "8 years from start of repayment",
        "years_remaining": years_remaining,
        "eligible_persons": ["Self", "Spouse", "Children", "Legal ward"],
        "note": "Full interest amount is deductible. No principal deduction."
    }


# ============================================================
# SECTION 80EE/80EEA - HOME LOAN INTEREST
# ============================================================

SECTION_80EE_LIMIT = 50000       # First-time home buyers (FY 2016-17 onwards)
SECTION_80EEA_LIMIT = 150000     # Affordable housing (FY 2019-20 to FY 2021-22)


def calculate_home_loan_interest_deduction(
    home_loan_interest: float,
    property_value: float = None,
    is_first_home: bool = True,
    sanction_date: str = None,
    claimed_24b: float = None
) -> dict:
    """
    Calculate home loan interest deductions under Section 24(b), 80EE, and 80EEA.
    
    Args:
        home_loan_interest: Total interest on home loan
        property_value: Value of property
        is_first_home: Whether this is first home purchase
        sanction_date: Loan sanction date (YYYY-MM-DD)
        claimed_24b: Amount already claimed under 24(b)
        
    Returns:
        Dictionary with home loan interest deduction breakdown
    """
    # Section 24(b) - Standard home loan interest deduction
    # ₹2,00,000 for self-occupied property
    # No limit for let-out property
    section_24b_self_occupied = min(home_loan_interest, 200000)
    
    deductions = {
        "section_24b": {
            "limit": 200000,
            "deduction": section_24b_self_occupied,
            "note": "For self-occupied property. No limit for let-out."
        },
        "section_80ee": {
            "available": False,
            "deduction": 0,
            "note": "First-time home buyer (FY 2016-17 to FY 2021-22)"
        },
        "section_80eea": {
            "available": False,
            "deduction": 0,
            "note": "Affordable housing scheme"
        }
    }
    
    return {
        "home_loan_interest": home_loan_interest,
        "deductions": deductions,
        "total_interest_deduction": section_24b_self_occupied,
        "note": "Section 24(b) available in both regimes. 80EE/80EEA only in Old regime."
    }


# ============================================================
# SECTION 80G - DONATIONS
# ============================================================

def calculate_80g_deduction(
    donations: List[Dict[str, float]],
    eligible_donations_100: float = 0,
    eligible_donations_50: float = 0
) -> dict:
    """
    Calculate Section 80G deduction for donations.
    
    Args:
        donations: List of donations with {'name': str, 'amount': float, 'type': str}
        eligible_donations_100: Donations eligible for 100% deduction
        eligible_donations_50: Donations eligible for 50% deduction
        
    Returns:
        Dictionary with donation deductions
    """
    # 100% deduction donations (PM Relief Fund, etc.)
    # 50% deduction donations (charitable institutions, etc.)
    
    deduction_100 = eligible_donations_100
    deduction_50 = eligible_donations_50 * 0.50
    
    total_deduction = deduction_100 + deduction_50
    
    return {
        "donations": donations,
        "100_percent_deduction": {
            "eligible": eligible_donations_100,
            "deduction": deduction_100,
            "examples": ["PM Relief Fund", "National Defence Fund", "Approved charities"]
        },
        "50_percent_deduction": {
            "eligible": eligible_donations_50,
            "deduction": deduction_50,
            "examples": ["Charitable institutions", "Educational institutions"]
        },
        "total_deduction": total_deduction,
        "note": "Some donations have qualifying limits (10% of adjusted gross total income)"
    }


# ============================================================
# COMPREHENSIVE DEDUCTION CALCULATOR
# ============================================================

def calculate_total_deductions(
    is_old_regime: bool = True,
    **kwargs
) -> dict:
    """
    Calculate all applicable deductions.
    
    Note: Many deductions are NOT available under New Tax Regime.
    Only the following are available in New Regime:
    - Standard Deduction (₹75,000)
    - Section 80CCD(2) - Employer NPS contribution
    - Section 80CCH(2) - Agniveer Corpus Fund
    - Section 10(10) - Gratuity
    - Section 10(10AA) - Leave Encashment
    - Professional Tax
    
    Args:
        is_old_regime: Whether using Old Tax Regime
        **kwargs: Various deduction inputs
        
    Returns:
        Dictionary with all deductions
    """
    if not is_old_regime:
        # New regime - limited deductions
        return {
            "regime": "NEW",
            "standard_deduction": 75000,
            "employer_nps_80ccd2": kwargs.get("employer_nps", 0),
            "other_deductions": 0,
            "total_deductions": 75000 + kwargs.get("employer_nps", 0),
            "note": "New regime has limited deductions. Most 80-series deductions not available."
        }
    
    # Old regime - full deductions
    deductions_80c = calculate_80c_deduction(**{
        k: v for k, v in kwargs.items() 
        if k in ['ppf', 'epf', 'elss', 'nsc', 'ssy', 'scss', 
                 'tax_saving_fd', 'nps_tier1', 'life_insurance_premium',
                 'home_loan_principal', 'tuition_fees', 'stamp_duty']
    })
    
    deductions_80d = calculate_80d_deduction(**{
        k: v for k, v in kwargs.items()
        if k in ['self_health_insurance', 'parents_health_insurance',
                 'self_age', 'parents_age', 'preventive_checkup_expense',
                 'self_is_senior', 'parents_are_senior']
    })
    
    hra_result = calculate_hra_exemption(**{
        k: v for k, v in kwargs.items()
        if k in ['hra_received', 'basic_salary', 'rent_paid', 'metro_city']
    }) if kwargs.get('hra_received') else None
    
    total = (
        50000 +  # Standard deduction (Old regime)
        deductions_80c['allowed_deduction'] +
        deductions_80d['total_deduction'] +
        (hra_result['hra_exemption'] if hra_result else 0) +
        kwargs.get('nps_additional_80ccd1b', 0) +
        kwargs.get('home_loan_interest', 0) +
        kwargs.get('education_loan_interest', 0) +
        kwargs.get('donations_80g', 0)
    )
    
    return {
        "regime": "OLD",
        "standard_deduction": 50000,
        "section_80c": deductions_80c,
        "section_80d": deductions_80d,
        "hra_exemption": hra_result,
        "other_deductions": {
            "80ccd1b_nps": kwargs.get('nps_additional_80ccd1b', 0),
            "80e_education_loan": kwargs.get('education_loan_interest', 0),
            "24b_home_loan_interest": kwargs.get('home_loan_interest', 0),
            "80g_donations": kwargs.get('donations_80g', 0),
        },
        "total_deductions": total,
    }


# ============================================================
# EXAMPLE USAGE
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("KARVID DEDUCTION CALCULATOR - FY 2025-26")
    print("=" * 60)
    
    # Example 80C calculation
    result_80c = calculate_80c_deduction(
        ppf=100000,
        epf=36000,
        elss=50000,
        life_insurance_premium=25000,
        home_loan_principal=80000
    )
    print("\n📊 SECTION 80C DEDUCTION:")
    print(f"   Total Claimed: ₹{result_80c['total_claimed']:,.0f}")
    print(f"   Allowed Deduction: ₹{result_80c['allowed_deduction']:,.0f}")
    print(f"   Unused Limit: ₹{result_80c['unused_limit']:,.0f}")
    
    # Example 80D calculation
    result_80d = calculate_80d_deduction(
        self_health_insurance=20000,
        parents_health_insurance=30000,
        self_age=35,
        parents_age=65,
        preventive_checkup_expense=5000
    )
    print("\n📊 SECTION 80D DEDUCTION:")
    print(f"   Self Health Insurance: ₹{result_80d['self_health_insurance']['allowed']:,.0f}")
    print(f"   Parents Health Insurance: ₹{result_80d['parents_health_insurance']['allowed']:,.0f}")
    print(f"   Total: ₹{result_80d['total_deduction']:,.0f}")
    
    # Example HRA calculation
    result_hra = calculate_hra_exemption(
        hra_received=120000,
        basic_salary=600000,
        rent_paid=180000,
        metro_city=True
    )
    print("\n📊 HRA EXEMPTION:")
    print(f"   HRA Received: ₹{result_hra['hra_received']:,.0f}")
    print(f"   Exemption: ₹{result_hra['hra_exemption']:,.0f}")
    print(f"   Taxable HRA: ₹{result_hra['taxable_hra']:,.0f}")
    
    print("\n" + "=" * 60)
