"""
KarVid - Tax Wizard Agent
Indian tax calculations and deductions
"""

from .tax_calculator import (
    KarVidTaxCalculator,
    calculate_new_regime_tax,
    calculate_old_regime_tax,
    compare_regimes,
)
from .deductions import (
    calculate_80c_deduction,
    calculate_80d_deduction,
    calculate_total_deductions,
)
from .capital_gains import (
    calculate_capital_gains,
    calculate_equity_ltcg,
)
from .indian_tax_laws import (
    INCOME_TAX_SECTIONS,
    CAPITAL_GAINS,
    TAX_SLABS,
    SEBI_REGULATIONS,
    get_tax_section_info,
    get_capital_gains_info,
    get_tax_slab,
)

__all__ = [
    'KarVidTaxCalculator',
    'calculate_new_regime_tax',
    'calculate_old_regime_tax',
    'compare_regimes',
    'calculate_80c_deduction',
    'calculate_80d_deduction',
    'calculate_total_deductions',
    'calculate_capital_gains',
    'calculate_equity_ltcg',
    'INCOME_TAX_SECTIONS',
    'CAPITAL_GAINS',
    'TAX_SLABS',
    'SEBI_REGULATIONS',
    'get_tax_section_info',
    'get_capital_gains_info',
    'get_tax_slab',
]
