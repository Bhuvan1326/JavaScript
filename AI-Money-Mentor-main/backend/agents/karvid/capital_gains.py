"""
KarVid Agent - Capital Gains Tax Module
Indian Capital Gains Taxation for FY 2025-26

This module covers:
- Short-Term Capital Gains (STCG) - held < 12/24/36 months
- Long-Term Capital Gains (LTCG) - held >= 12/24/36 months
- Tax rates for Equity, Debt, Mutual Funds, Real Estate
- Grandfathering provisions
- Indexation benefits (where applicable)
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple
from enum import Enum
from datetime import datetime


# ============================================================
# HOLDING PERIODS (as per Budget 2024)
# ============================================================

class HoldingPeriod(Enum):
    """Minimum holding period for LTCG classification"""
    EQUITY_SHARES = 12       # Listed equity shares: 12 months
    EQUITY_MF = 12           # Listed equity mutual funds: 12 months
    DEBT_MF = 24             # Debt mutual funds (>65% debt): 24 months
    UNLISTED_SHARES = 24     # Unlisted shares: 24 months
    IMMOVABLE_PROPERTY = 24  # Real estate: 24 months
    LISTED_BONDS = 12        # Listed bonds/debentures: 12 months
    UNLISTED_BONDS = 24      # Unlisted bonds/debentures: 24 months
    GOLD_ETF = 12            # Gold ETFs: 12 months
    OTHER_ASSETS = 36        # Other assets: 36 months


# ============================================================
# CAPITAL GAINS TAX RATES (FY 2025-26)
# ============================================================

# STCG Rates
STCG_RATES = {
    "listed_equity": 0.20,           # 20% (STT paid)
    "equity_mf": 0.20,               # 20% (STT paid)
    "debt_mf_spec": None,            # At slab rate (acquired on/after Apr 1, 2023)
    "debt_mf_old": 0.125,            # 12.5% (acquired before Apr 1, 2023)
    "unlisted_shares": None,         # At slab rate
    "immovable_property": None,      # At slab rate
    "listed_bonds": None,            # At slab rate
    "unlisted_bonds": None,          # At slab rate
}

# LTCG Rates
LTCG_RATES = {
    "listed_equity": {
        "rate": 0.125,               # 12.5%
        "exemption": 125000,         # ₹1.25 Lakh exemption
        "indexation": False,
    },
    "equity_mf": {
        "rate": 0.125,               # 12.5%
        "exemption": 125000,         # ₹1.25 Lakh exemption
        "indexation": False,
    },
    "debt_mf_spec": {
        "rate": None,                # At slab rate (acquired on/after Apr 1, 2023)
        "exemption": 0,
        "indexation": False,
    },
    "debt_mf_old": {
        "rate": 0.125,               # 12.5% (acquired before Apr 1, 2023)
        "exemption": 0,
        "indexation": False,
    },
    "unlisted_shares": {
        "rate": 0.125,               # 12.5%
        "exemption": 0,
        "indexation": False,
    },
    "immovable_property": {
        "rate": 0.125,               # 12.5% (without indexation)
        "exemption": 0,
        "indexation": False,         # No indexation for properties acquired after July 23, 2024
    },
    "immovable_property_old": {
        "rate": 0.20,                # 20% with indexation OR 12.5% without
        "exemption": 0,
        "indexation": True,          # Indexation available for properties before July 23, 2024
    },
    "listed_bonds": {
        "rate": 0.125,               # 12.5%
        "exemption": 0,
        "indexation": False,
    },
    "unlisted_bonds": {
        "rate": None,                # At slab rate
        "exemption": 0,
        "indexation": False,
    },
}

# Grandfathering date for equity LTCG
GRANDFATHERING_DATE = datetime(2018, 2, 1)


@dataclass
class CapitalGainsResult:
    """Result of capital gains calculation"""
    asset_type: str
    holding_period_days: int
    is_long_term: bool
    purchase_price: float
    sale_price: float
    capital_gain: float
    exemption: float
    taxable_gain: float
    tax_rate: float
    tax_amount: float
    cess: float
    total_tax: float


def determine_holding_type(days_held: int, asset_type: str) -> str:
    """
    Determine if gain is STCG or LTCG based on holding period.
    
    Args:
        days_held: Number of days asset was held
        asset_type: Type of asset
        
    Returns:
        'STCG' or 'LTCG'
    """
    holding_periods = {
        "listed_equity": 365,
        "equity_mf": 365,
        "debt_mf": 730,  # 24 months for debt MFs
        "unlisted_shares": 730,
        "immovable_property": 730,
        "listed_bonds": 365,
        "unlisted_bonds": 730,
        "gold_etf": 365,
    }
    
    threshold = holding_periods.get(asset_type, 365)
    return "LTCG" if days_held >= threshold else "STCG"


def calculate_equity_ltcg(
    sale_price: float,
    purchase_price: float,
    days_held: int,
    purchase_date: datetime = None,
    stt_paid: bool = True
) -> CapitalGainsResult:
    """
    Calculate LTCG for listed equity shares and equity mutual funds.
    
    For FY 2025-26:
    - LTCG rate: 12.5%
    - Exemption: ₹1.25 Lakh
    - No indexation benefit
    
    Args:
        sale_price: Total sale consideration
        purchase_price: Purchase cost
        days_held: Number of days held
        purchase_date: Date of purchase (for grandfathering)
        stt_paid: Whether STT was paid on transaction
        
    Returns:
        CapitalGainsResult object
    """
    # Determine if LTCG
    is_long_term = days_held >= 365
    
    if not is_long_term:
        # STCG on equity: 20%
        capital_gain = sale_price - purchase_price
        tax_rate = 0.20 if stt_paid else None  # At slab if no STT
        tax_amount = capital_gain * tax_rate if tax_rate else 0
        cess = tax_amount * 0.04
        
        return CapitalGainsResult(
            asset_type="listed_equity",
            holding_period_days=days_held,
            is_long_term=False,
            purchase_price=purchase_price,
            sale_price=sale_price,
            capital_gain=capital_gain,
            exemption=0,
            taxable_gain=capital_gain if capital_gain > 0 else 0,
            tax_rate=tax_rate or 0,
            tax_amount=tax_amount if capital_gain > 0 else 0,
            cess=cess if capital_gain > 0 else 0,
            total_tax=(tax_amount + cess) if capital_gain > 0 else 0
        )
    
    # LTCG calculation
    capital_gain = sale_price - purchase_price
    
    # Apply exemption (₹1.25 Lakh)
    exemption_limit = 125000
    exemption = min(capital_gain, exemption_limit) if capital_gain > 0 else 0
    taxable_gain = max(0, capital_gain - exemption)
    
    # Tax at 12.5%
    tax_rate = 0.125
    tax_amount = taxable_gain * tax_rate
    cess = tax_amount * 0.04  # Health & Education Cess
    
    return CapitalGainsResult(
        asset_type="listed_equity",
        holding_period_days=days_held,
        is_long_term=True,
        purchase_price=purchase_price,
        sale_price=sale_price,
        capital_gain=capital_gain,
        exemption=exemption,
        taxable_gain=taxable_gain,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        cess=cess,
        total_tax=tax_amount + cess
    )


def calculate_debt_mf_capital_gains(
    sale_price: float,
    purchase_price: float,
    days_held: int,
    purchase_date: datetime,
    acquisition_date: datetime = None
) -> CapitalGainsResult:
    """
    Calculate capital gains for Debt Mutual Funds.
    
    Important: Budget 2023 changes
    - Funds acquired on/after Apr 1, 2023 (>65% in debt):
      - Treated as STCG regardless of holding period
      - Taxed at slab rates
    - Funds acquired before Apr 1, 2023:
      - STCG: 12.5% without indexation
      - LTCG: 12.5% without indexation (after 24 months)
    
    Args:
        sale_price: Total sale consideration
        purchase_price: Purchase cost
        days_held: Number of days held
        purchase_date: Date of purchase
        acquisition_date: Alternative date for acquisition
        
    Returns:
        CapitalGainsResult object
    """
    purchase_dt = acquisition_date or purchase_date
    budget_2023_cutoff = datetime(2023, 4, 1)
    is_new_regime = purchase_dt >= budget_2023_cutoff if purchase_dt else True
    
    capital_gain = sale_price - purchase_price
    is_long_term = days_held >= 730  # 24 months for debt MF
    
    if is_new_regime:
        # Acquired on/after Apr 1, 2023 - Taxed at slab rate
        # No LTCG benefit, treated as STCG
        return CapitalGainsResult(
            asset_type="debt_mf",
            holding_period_days=days_held,
            is_long_term=False,  # Always STCG for new regime
            purchase_price=purchase_price,
            sale_price=sale_price,
            capital_gain=capital_gain,
            exemption=0,
            taxable_gain=capital_gain if capital_gain > 0 else 0,
            tax_rate=0,  # At slab rate
            tax_amount=0,  # Will be added to income
            cess=0,
            total_tax=0,  # Taxed at slab
            note="Taxed at applicable slab rate - no LTCG benefit"
        )
    
    # Old regime - before Apr 1, 2023
    tax_rate = 0.125  # 12.5%
    tax_amount = abs(capital_gain) * tax_rate if capital_gain > 0 else 0
    cess = tax_amount * 0.04
    
    return CapitalGainsResult(
        asset_type="debt_mf",
        holding_period_days=days_held,
        is_long_term=is_long_term,
        purchase_price=purchase_price,
        sale_price=sale_price,
        capital_gain=capital_gain,
        exemption=0,
        taxable_gain=capital_gain if capital_gain > 0 else 0,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        cess=cess,
        total_tax=tax_amount + cess
    )


def calculate_real_estate_capital_gains(
    sale_price: float,
    purchase_price: float,
    days_held: int,
    purchase_date: datetime,
    indexed_cost: float = None,
    use_indexation: bool = False
) -> CapitalGainsResult:
    """
    Calculate capital gains for immovable property (real estate).
    
    For properties acquired BEFORE July 23, 2024:
    - Option: 20% with indexation OR 12.5% without indexation
    - Choose whichever gives lower tax
    
    For properties acquired ON/After July 23, 2024:
    - LTCG: 12.5% without indexation
    
    Args:
        sale_price: Total sale consideration
        purchase_price: Purchase cost
        days_held: Number of days held
        purchase_date: Date of purchase
        indexed_cost: Cost with indexation applied (if available)
        use_indexation: Whether to use indexation (for old properties)
        
    Returns:
        CapitalGainsResult object
    """
    is_long_term = days_held >= 730  # 24 months
    capital_gain = sale_price - purchase_price
    budget_2024_cutoff = datetime(2024, 7, 23)
    is_old_property = purchase_date < budget_2024_cutoff if purchase_date else False
    
    if not is_long_term:
        # STCG - taxed at slab rates
        return CapitalGainsResult(
            asset_type="immovable_property",
            holding_period_days=days_held,
            is_long_term=False,
            purchase_price=purchase_price,
            sale_price=sale_price,
            capital_gain=capital_gain,
            exemption=0,
            taxable_gain=capital_gain if capital_gain > 0 else 0,
            tax_rate=0,  # At slab rate
            tax_amount=0,
            cess=0,
            total_tax=0,
            note="STCG taxed at applicable slab rate"
        )
    
    # LTCG calculation
    if is_old_property and use_indexation and indexed_cost:
        # Option 1: 20% with indexation
        indexed_gain = sale_price - indexed_cost
        tax_with_indexation = indexed_gain * 0.20
        cess1 = tax_with_indexation * 0.04
        
        # Option 2: 12.5% without indexation
        tax_without_indexation = capital_gain * 0.125
        cess2 = tax_without_indexation * 0.04
        
        # Choose lower
        if (tax_with_indexation + cess1) < (tax_without_indexation + cess2):
            return CapitalGainsResult(
                asset_type="immovable_property",
                holding_period_days=days_held,
                is_long_term=True,
                purchase_price=purchase_price,
                sale_price=sale_price,
                capital_gain=indexed_gain,
                exemption=0,
                taxable_gain=indexed_gain,
                tax_rate=0.20,
                tax_amount=tax_with_indexation,
                cess=cess1,
                total_tax=tax_with_indexation + cess1,
                note="20% with indexation chosen (lower tax)"
            )
    
    # Default: 12.5% without indexation
    tax_rate = 0.125
    tax_amount = capital_gain * tax_rate if capital_gain > 0 else 0
    cess = tax_amount * 0.04
    
    return CapitalGainsResult(
        asset_type="immovable_property",
        holding_period_days=days_held,
        is_long_term=True,
        purchase_price=purchase_price,
        sale_price=sale_price,
        capital_gain=capital_gain,
        exemption=0,
        taxable_gain=capital_gain if capital_gain > 0 else 0,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        cess=cess,
        total_tax=tax_amount + cess
    )


def calculate_unlisted_shares_capital_gains(
    sale_price: float,
    purchase_price: float,
    days_held: int
) -> CapitalGainsResult:
    """
    Calculate capital gains for unlisted shares (startups, private equity).
    
    STCG (held < 24 months): Taxed at slab rates
    LTCG (held >= 24 months): 12.5% without indexation
    
    Args:
        sale_price: Total sale consideration
        purchase_price: Purchase cost
        days_held: Number of days held
        
    Returns:
        CapitalGainsResult object
    """
    capital_gain = sale_price - purchase_price
    is_long_term = days_held >= 730  # 24 months
    
    if not is_long_term:
        # STCG - at slab rates
        return CapitalGainsResult(
            asset_type="unlisted_shares",
            holding_period_days=days_held,
            is_long_term=False,
            purchase_price=purchase_price,
            sale_price=sale_price,
            capital_gain=capital_gain,
            exemption=0,
            taxable_gain=capital_gain if capital_gain > 0 else 0,
            tax_rate=0,  # At slab rate
            tax_amount=0,
            cess=0,
            total_tax=0,
            note="STCG taxed at applicable slab rate"
        )
    
    # LTCG - 12.5% without indexation
    tax_rate = 0.125
    tax_amount = capital_gain * tax_rate if capital_gain > 0 else 0
    cess = tax_amount * 0.04
    
    return CapitalGainsResult(
        asset_type="unlisted_shares",
        holding_period_days=days_held,
        is_long_term=True,
        purchase_price=purchase_price,
        sale_price=sale_price,
        capital_gain=capital_gain,
        exemption=0,
        taxable_gain=capital_gain if capital_gain > 0 else 0,
        tax_rate=tax_rate,
        tax_amount=tax_amount,
        cess=cess,
        total_tax=tax_amount + cess
    )


def calculate_capital_gains(
    asset_type: str,
    sale_price: float,
    purchase_price: float,
    days_held: int,
    purchase_date: datetime = None,
    **kwargs
) -> CapitalGainsResult:
    """
    Universal capital gains calculator.
    
    Args:
        asset_type: 'equity', 'equity_mf', 'debt_mf', 'real_estate', 'unlisted_shares'
        sale_price: Sale consideration
        purchase_price: Purchase cost
        days_held: Days asset was held
        purchase_date: Date of purchase
        **kwargs: Additional parameters (indexed_cost, use_indexation, stt_paid, etc.)
        
    Returns:
        CapitalGainsResult object
    """
    asset_type_lower = asset_type.lower()
    
    if asset_type_lower in ['equity', 'listed_equity', 'equity_mf', 'equity_mutual_fund']:
        return calculate_equity_ltcg(
            sale_price=sale_price,
            purchase_price=purchase_price,
            days_held=days_held,
            purchase_date=purchase_date,
            stt_paid=kwargs.get('stt_paid', True)
        )
    
    elif asset_type_lower in ['debt_mf', 'debt_mutual_fund']:
        return calculate_debt_mf_capital_gains(
            sale_price=sale_price,
            purchase_price=purchase_price,
            days_held=days_held,
            purchase_date=purchase_date
        )
    
    elif asset_type_lower in ['real_estate', 'immovable_property', 'property']:
        return calculate_real_estate_capital_gains(
            sale_price=sale_price,
            purchase_price=purchase_price,
            days_held=days_held,
            purchase_date=purchase_date,
            indexed_cost=kwargs.get('indexed_cost'),
            use_indexation=kwargs.get('use_indexation', False)
        )
    
    elif asset_type_lower in ['unlisted_shares', 'startup_shares', 'private_equity']:
        return calculate_unlisted_shares_capital_gains(
            sale_price=sale_price,
            purchase_price=purchase_price,
            days_held=days_held
        )
    
    else:
        # Default: treat as other asset
        is_long_term = days_held >= 365
        capital_gain = sale_price - purchase_price
        
        return CapitalGainsResult(
            asset_type=asset_type,
            holding_period_days=days_held,
            is_long_term=is_long_term,
            purchase_price=purchase_price,
            sale_price=sale_price,
            capital_gain=capital_gain,
            exemption=0,
            taxable_gain=capital_gain if capital_gain > 0 else 0,
            tax_rate=0.20 if is_long_term else 0,
            tax_amount=abs(capital_gain) * 0.20 if is_long_term and capital_gain > 0 else 0,
            cess=0,
            total_tax=abs(capital_gain) * 0.20 * 1.04 if is_long_term and capital_gain > 0 else 0,
            note=f"Generic calculation for {asset_type}"
        )


# ============================================================
# SECTION 54 EXEMPTIONS (Reinvestment)
# ============================================================

def calculate_section_54_exemption(
    capital_gain: float,
    reinvested_amount: float,
    exemption_type: str = "residential_property"
) -> dict:
    """
    Calculate exemption under Section 54 series for reinvestment.
    
    Section 54: LTCG from residential property reinvested in residential property
    Section 54F: LTCG from any asset reinvested in residential property
    Section 54EC: LTCG reinvested in specified bonds (max ₹50L)
    
    Args:
        capital_gain: Long-term capital gain amount
        reinvested_amount: Amount reinvested
        exemption_type: Type of exemption (54, 54F, 54EC)
        
    Returns:
        Dictionary with exemption details
    """
    exemptions = {
        "54": {
            "name": "Section 54",
            "description": "LTCG from residential property reinvested in new residential property",
            "max_limit": None,
            "holding_period": 3,  # years
        },
        "54f": {
            "name": "Section 54F",
            "description": "LTCG from any capital asset reinvested in residential property",
            "max_limit": None,
            "holding_period": 3,
            "condition": "Entire sale proceeds must be reinvested for full exemption",
        },
        "54ec": {
            "name": "Section 54EC",
            "description": "LTCG reinvested in specified bonds (NHAI/RECL)",
            "max_limit": 50000000,  # ₹50 Lakh
            "holding_period": 5,
            "investment_period": 6,  # months from sale
        },
    }
    
    if exemption_type.lower() in ["54", "residential_property"]:
        # Full exemption if entire gain reinvested
        exemption = min(capital_gain, reinvested_amount)
        return {
            "section": "54",
            "capital_gain": capital_gain,
            "reinvested_amount": reinvested_amount,
            "exemption": exemption,
            "taxable_gain": max(0, capital_gain - reinvested_amount),
            "conditions": [
                "New property must be purchased within 1 year before or 2 years after sale",
                "Or constructed within 3 years",
                "New property must not be sold for 3 years"
            ]
        }
    
    elif exemption_type.lower() in ["54f", "any_asset"]:
        # Exemption proportional to reinvestment
        exemption = min(capital_gain, reinvested_amount)
        return {
            "section": "54F",
            "capital_gain": capital_gain,
            "reinvested_amount": reinvested_amount,
            "exemption": exemption,
            "taxable_gain": max(0, capital_gain - reinvested_amount),
            "conditions": [
                "Entire sale proceeds must be reinvested for full exemption",
                "Only one residential property can be owned (excluding new one)",
                "New property must be purchased within 1 year before or 2 years after sale",
                "Or constructed within 3 years"
            ]
        }
    
    elif exemption_type.lower() in ["54ec", "bonds"]:
        # Max ₹50 Lakh investment in specified bonds
        max_investment = exemptions["54ec"]["max_limit"]
        eligible_investment = min(reinvested_amount, max_investment)
        exemption = min(capital_gain, eligible_investment)
        
        return {
            "section": "54EC",
            "capital_gain": capital_gain,
            "reinvested_amount": reinvested_amount,
            "max_investment": max_investment,
            "exemption": exemption,
            "taxable_gain": max(0, capital_gain - exemption),
            "conditions": [
                "Investment must be made within 6 months of sale",
                "Maximum investment: ₹50 Lakh per financial year",
                "Lock-in period: 5 years",
                "Eligible bonds: NHAI, RECL, etc."
            ]
        }
    
    return {"error": "Invalid exemption type"}


# ============================================================
# EXAMPLE USAGE
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("KARVID CAPITAL GAINS TAX CALCULATOR - FY 2025-26")
    print("=" * 70)
    
    # Example 1: Equity LTCG
    print("\n📊 EXAMPLE 1: Listed Equity Shares (LTCG)")
    result = calculate_capital_gains(
        asset_type="equity",
        sale_price=500000,
        purchase_price=300000,
        days_held=500,
        stt_paid=True
    )
    print(f"   Sale Price: ₹{result.sale_price:,.0f}")
    print(f"   Purchase Price: ₹{result.purchase_price:,.0f}")
    print(f"   Capital Gain: ₹{result.capital_gain:,.0f}")
    print(f"   Exemption: ₹{result.exemption:,.0f}")
    print(f"   Taxable Gain: ₹{result.taxable_gain:,.0f}")
    print(f"   Tax Rate: {result.tax_rate*100:.1f}%")
    print(f"   Tax Amount: ₹{result.tax_amount:,.0f}")
    print(f"   Cess (4%): ₹{result.cess:,.0f}")
    print(f"   Total Tax: ₹{result.total_tax:,.0f}")
    
    # Example 2: Equity STCG
    print("\n📊 EXAMPLE 2: Listed Equity Shares (STCG)")
    result = calculate_capital_gains(
        asset_type="equity",
        sale_price=500000,
        purchase_price=400000,
        days_held=180,
        stt_paid=True
    )
    print(f"   Holding Period: {result.holding_period_days} days (Short Term)")
    print(f"   Capital Gain: ₹{result.capital_gain:,.0f}")
    print(f"   Tax Rate: {result.tax_rate*100:.0f}%")
    print(f"   Total Tax: ₹{result.total_tax:,.0f}")
    
    # Example 3: Real Estate LTCG
    print("\n📊 EXAMPLE 3: Real Estate (LTCG)")
    from datetime import datetime, timedelta
    result = calculate_capital_gains(
        asset_type="real_estate",
        sale_price=10000000,
        purchase_price=4000000,
        days_held=1500,
        purchase_date=datetime(2020, 1, 1)
    )
    print(f"   Sale Price: ₹{result.sale_price:,.0f}")
    print(f"   Purchase Price: ₹{result.purchase_price:,.0f}")
    print(f"   Capital Gain: ₹{result.capital_gain:,.0f}")
    print(f"   Tax Rate: {result.tax_rate*100:.1f}%")
    print(f"   Total Tax: ₹{result.total_tax:,.0f}")
    
    # Example 4: Section 54EC Exemption
    print("\n📊 EXAMPLE 4: Section 54EC Exemption (Bond Investment)")
    exemption_result = calculate_section_54_exemption(
        capital_gain=2000000,
        reinvested_amount=2000000,
        exemption_type="54ec"
    )
    print(f"   Capital Gain: ₹{exemption_result['capital_gain']:,.0f}")
    print(f"   Reinvested in Bonds: ₹{exemption_result['reinvested_amount']:,.0f}")
    print(f"   Exemption: ₹{exemption_result['exemption']:,.0f}")
    print(f"   Taxable Gain: ₹{exemption_result['taxable_gain']:,.0f}")
    
    print("\n" + "=" * 70)
    print("⚠️  NOTE: Section 87A rebate NOT applicable on capital gains tax")
    print("⚠️  STCG from equity taxed at 20% (special rate)")
    print("⚠️  LTCG from equity taxed at 12.5% (₹1.25L exemption)")
    print("=" * 70)
