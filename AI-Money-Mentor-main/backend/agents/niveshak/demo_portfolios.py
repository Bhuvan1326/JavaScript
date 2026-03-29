"""
Demo portfolio data for testing
All calculations are real-time - only initial data is provided
"""

from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta
import random

@dataclass
class PortfolioSchemes:
    name: str
    amc: str
    nav: float
    units: float
    isin: str

def get_demo_portfolios():
    """Return demo portfolios for different risk profiles"""
    return {
        "conservative": [
            {"name": "HDFC Liquid Fund - Direct Plan - Growth", "amc": "HDFC AMC", "nav": 2150.45, "units": 500, "isin": "INF17VJ01XX"},
            {"name": "ICICI Prudential Short Term Fund - Direct Plan", "amc": "ICICI Pru AMC", "nav": 52.34, "units": 1000, "isin": "INF459K01YY"},
            {"name": "SBI Magnum Gilt Fund - Direct Plan", "amc": "SBI MF", "nav": 58.92, "units": 800, "isin": "INF459K01ZZ"},
            {"name": "Axis Low Duration Fund - Direct Plan", "amc": "Axis AMC", "nav": 1250.67, "units": 400, "isin": "INF846K01AA"},
            {"name": "Kotak Bond Fund - Direct Plan", "amc": "Kotak AMC", "nav": 42.18, "units": 1500, "isin": "INF174K01BB"},
        ],
        "balanced": [
            {"name": "Axis Bluechip Fund - Direct Plan - Growth", "amc": "Axis AMC", "nav": 52.34, "units": 1500, "isin": "INF846K011N2"},
            {"name": "Parag Parikh Flexi Cap Fund - Direct Plan", "amc": "PPFAS AMC", "nav": 68.92, "units": 800, "isin": "INF223J011Y9"},
            {"name": "Mirae Asset Large Cap Fund - Direct Plan", "amc": "Mirae AMC", "nav": 85.45, "units": 600, "isin": "INF602I010XX"},
            {"name": "ICICI Prudential Technology Fund - Direct Plan", "amc": "ICICI Pru AMC", "nav": 168.23, "units": 350, "isin": "INF459K01EH6"},
            {"name": "HDFC Index Fund - Nifty 50 Plan - Direct Plan", "amc": "HDFC AMC", "nav": 185.67, "units": 500, "isin": "INF17VJ011X3"},
        ],
        "aggressive": [
            {"name": "Quant Small Cap Fund - Direct Plan - Growth", "amc": "Quant AMC", "nav": 180.45, "units": 700, "isin": "INF459K01SC"},
            {"name": "ICICI Prudential Technology Fund - Direct Plan", "amc": "ICICI Pru AMC", "nav": 168.23, "units": 900, "isin": "INF459K01EH6"},
            {"name": "Nippon India Small Cap Fund - Direct Plan", "amc": "Nippon AMC", "nav": 125.67, "units": 1200, "isin": "INF204K01SM"},
            {"name": "Tata Digital India Fund - Direct Plan", "amc": "Tata AMC", "nav": 48.34, "units": 2000, "isin": "INF204K01DI"},
            {"name": "SBI Contra Fund - Direct Plan - Growth", "amc": "SBI MF", "nav": 285.12, "units": 600, "isin": "INF459K01CT"},
            {"name": "Kotak Emerging Equity Fund - Direct Plan", "amc": "Kotak AMC", "nav": 92.45, "units": 1000, "isin": "INF174K01EE"},
        ],
    }
