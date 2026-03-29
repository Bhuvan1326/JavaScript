"""
SEBI Compliance Module
Regulatory disclaimers and compliance information
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Disclaimer:
    """Disclaimer content"""
    title: str
    content: str
    category: str


class SEBICompliance:
    """
    SEBI Compliance and Disclaimers
    
    Provides regulatory information required for
    financial advisory services in India
    """
    
    DISCLAIMERS: List[Disclaimer] = [
        Disclaimer(
            title="Investment Advisory",
            content="This platform provides educational information only. It is not a SEBI-registered investment advisor. All investment decisions should be made after consulting with a SEBI-registered investment advisor.",
            category="general"
        ),
        Disclaimer(
            title="Mutual Funds",
            content="Mutual fund investments are subject to market risks. Read all scheme related documents carefully. Past performance is not indicative of future results.",
            category="mf"
        ),
        Disclaimer(
            title="Stocks",
            content="Stock investments are subject to market risks. Equity investments carry high risk and volatility. This platform does not provide stock recommendations.",
            category="stocks"
        ),
        Disclaimer(
            title="Tax",
            content="Tax calculations are estimates based on current tax laws. Individual tax situations may vary. Please consult a tax professional for specific advice.",
            category="tax"
        ),
        Disclaimer(
            title="Financial Planning",
            content="Financial planning projections are based on assumptions and historical data. Actual results may vary significantly.",
            category="planning"
        ),
    ]
    
    @staticmethod
    def get_regulations() -> Dict:
        """Get key SEBI regulations"""
        return {
            "investment_adviser": {
                "act": "SEBI (Investment Advisers) Regulations, 2013",
                "registration_required": True,
                "requirements": [
                    "Qualification: NISM certification or equivalent",
                    "Experience: 5 years in financial services",
                    "Net worth: ₹2 crore for corporate, ₹5 lakh for individual",
                    "Compliance officer mandatory",
                ]
            },
            "mutual_funds": {
                "act": "SEBI (Mutual Funds) Regulations, 1996",
                "disclosures": [
                    "Offer document must be provided",
                    "Riskometer mandatory",
                    "NAV disclosure daily",
                    "Expense ratio disclosure",
                ]
            },
            "research_analyst": {
                "act": "SEBI (Research Analysts) Regulations, 2014",
                "requirements": [
                    "Registration with SEBI",
                    "Disclosure of conflicts of interest",
                    "Rating methodology disclosure",
                    "Compensation disclosure",
                ]
            }
        }
    
    @classmethod
    def get_disclaimers_by_category(cls, category: str = "all") -> List[Dict]:
        """Get disclaimers filtered by category"""
        if category == "all":
            return [{"title": d.title, "content": d.content, "category": d.category} 
                    for d in cls.DISCLAIMERS]
        
        return [{"title": d.title, "content": d.content, "category": d.category}
                for d in cls.DISCLAIMERS if d.category == category]
    
    @classmethod
    def get_full_disclaimer(cls) -> str:
        """Get full legal disclaimer"""
        disclaimers = "\n\n".join([f"{d.title}:\n{d.content}" for d in cls.DISCLAIMERS])
        
        return f"""
IMPORTANT LEGAL DISCLAIMER
=========================

{disclaimers}

REGULATORY FRAMEWORK
====================

This platform is for educational purposes only and does not:
- Provide personalized investment advice
- Recommend specific securities
- Guarantee returns
- Take custody of client assets

Users are advised to consult with qualified professionals before making any investment decisions.

SEBI Registration: NOT REQUIRED (Educational platform)
Jurisdiction: India
Last Updated: March 2026
"""


def get_disclaimers(category: str = "all") -> List[Dict]:
    """Convenience function to get disclaimers"""
    return SEBICompliance.get_disclaimers_by_category(category)
