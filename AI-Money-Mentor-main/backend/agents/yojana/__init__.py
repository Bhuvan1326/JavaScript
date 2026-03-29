"""
YojanaKarta Agent - Financial Planner
FIRE (Financial Independence, Retire Early) Calculator for India
"""

from .fire_calculator import (
    FIRECalculator,
    FIREPlan,
    FIREMethod,
    calculate_fire_number_india,
    get_sip_recommendation
)

__all__ = [
    'FIRECalculator',
    'FIREPlan',
    'FIREMethod',
    'calculate_fire_number_india',
    'get_sip_recommendation'
]
