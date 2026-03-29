"""
Vidhi - Legal/Compliance Agent
SEBI compliance, regulations, and legal knowledge
"""

from .compliance import (
    SEBICompliance,
    get_disclaimers,
)
from .legal_knowledge import (
    CONSTITUTION_PROVISIONS,
    INCOME_TAX_ACT,
    SEBI_ACTS,
    RBI_REGULATIONS,
    CONSUMER_PROTECTION,
    get_constitution_provision,
    get_income_tax_section,
    get_sebi_regulation,
    get_rbi_regulation,
    get_consumer_protection,
    get_legal_disclaimer,
)

__all__ = [
    'SEBICompliance',
    'get_disclaimers',
    'CONSTITUTION_PROVISIONS',
    'INCOME_TAX_ACT',
    'SEBI_ACTS',
    'RBI_REGULATIONS',
    'CONSUMER_PROTECTION',
    'get_constitution_provision',
    'get_income_tax_section',
    'get_sebi_regulation',
    'get_rbi_regulation',
    'get_consumer_protection',
    'get_legal_disclaimer',
]
