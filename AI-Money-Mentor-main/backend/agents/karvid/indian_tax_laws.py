"""
Indian Tax Laws - Comprehensive Knowledge Base
All tax rules from Indian Constitution and Income Tax Act
"""

# Income Tax Act Sections
INCOME_TAX_SECTIONS = {
    # Chapter VI-A Deductions
    "80C": {
        "limit": 150000,
        "description": "Deductions for investments and savings",
        "eligible_investments": [
            "PPF (Public Provident Fund)",
            "ELSS (Equity Linked Savings Scheme)",
            "NSC (National Savings Certificate)",
            "Tax-saving FD (5-year Fixed Deposit)",
            "NPS (National Pension System) - Tier 1",
            "Life Insurance Premium",
            "EPF (Employee Provident Fund)",
            "SSY (Sukanya Samriddhi Yojana)",
            "ULIP (Unit Linked Insurance Plan)",
            "Senior Citizen Savings Scheme",
            "Post Office TD (5-year Term Deposit)",
            "Home Loan Principal Repayment",
            "Children's Tuition Fees",
            "Sovereign Gold Bond",
        ]
    },
    "80CCD": {
        "1B": {
            "limit": 50000,
            "description": "Additional NPS contribution (self)",
        },
        "2": {
            "limit": "10% of salary (private) or 14% (govt)",
            "description": "Employer NPS contribution",
        }
    },
    "80D": {
        "limit": {
            "self_family": 25000,
            "senior_citizen": 50000,
            "parents": 25000,
            "parents_senior": 50000,
        },
        "description": "Health Insurance Premium",
        "preventive_health_checkup": 5000,
    },
    "80DD": {
        "limit": {
            "disability_40_80": 75000,
            "disability_80_plus": 125000,
        },
        "description": "Deduction for disabled dependent",
    },
    "80DDB": {
        "limit": {
            "below_60": 40000,
            "60_plus": 100000,
        },
        "description": "Medical treatment of specified diseases",
        "diseases": [
            "Neurological diseases",
            "Cancer",
            "AIDS",
            "Chronic renal failure",
            "Hemophilia",
            "Thalassemia",
        ]
    },
    "80E": {
        "limit": "No upper limit",
        "years": 8,
        "description": "Interest on Education Loan",
    },
    "80EE": {
        "limit": 50000,
        "description": "Interest on Home Loan (first home)",
        "conditions": [
            "Loan sanctioned between 1 Apr 2016 - 31 Mar 2022",
            "Property value ≤ ₹50 lakh",
            "Loan amount ≤ ₹35 lakh",
            "No other house owned",
        ]
    },
    "80EEA": {
        "limit": 150000,
        "description": "Additional interest on Home Loan",
        "conditions": [
            "Loan sanctioned between 1 Apr 2019 - 31 Mar 2022",
            "Stamp value ≤ ₹45 lakh",
            "No house in any other municipality",
        ]
    },
    "80G": {
        "description": "Donations to charitable institutions",
        "deduction": "50% to 100% depending on institution",
        "limit": "Varies by institution type",
    },
    "80GG": {
        "limit": "₹5,000/month or 25% of income (lower)",
        "description": "Rent paid (if no HRA)",
        "conditions": [
            "Not receiving HRA",
            "Not owning house in current location",
            "Not owning house anywhere else",
        ]
    },
    "80GGA": {
        "description": "Donations for scientific research",
        "deduction": "100%",
    },
    "80GGB": {
        "limit": "No limit",
        "description": "Donations to political parties (business)",
    },
    "80GGC": {
        "limit": "No limit",
        "description": "Donations to political parties (individuals)",
    },
    "80TTA": {
        "limit": 10000,
        "description": "Interest on Savings Account",
    },
    "80TTB": {
        "limit": 50000,
        "description": "Interest income for Senior Citizens",
    },
    "80U": {
        "limit": {
            "disability_40_80": 75000,
            "disability_80_plus": 125000,
        },
        "description": "Deduction for disabled individual (self)",
    },
}

# Capital Gains Tax Rules (FY 2025-26)
CAPITAL_GAINS = {
    "equity": {
        "LTCG": {
            "holding_period": "12+ months",
            "tax_rate": "12.5%",
            "exemption": 125000,
            "grandfathering": "No (removed)",
        },
        "STCG": {
            "holding_period": "<12 months",
            "tax_rate": "20%",
            "exemption": 0,
        }
    },
    "debt": {
        "LTCG": {
            "holding_period": "24+ months",
            "tax_rate": "12.5% with indexation",
            "exemption": 0,
        },
        "STCG": {
            "holding_period": "<24 months",
            "tax_rate": "Slab rate",
            "exemption": 0,
        }
    },
    "real_estate": {
        "LTCG": {
            "holding_period": "24+ months",
            "tax_rate": "12.5% with indexation",
            "exemption_options": [
                "Section 54: Invest in new house",
                "Section 54EC: Invest in bonds (NHAI/RECL)",
                "Section 54F: Invest in house from equity",
            ]
        },
        "STCG": {
            "holding_period": "<24 months",
            "tax_rate": "Slab rate",
        }
    },
    "gold": {
        "LTCG": {
            "holding_period": "24+ months",
            "tax_rate": "12.5% with indexation",
        },
        "STCG": {
            "holding_period": "<24 months",
            "tax_rate": "Slab rate",
        }
    }
}

# Tax Slabs (FY 2025-26)
TAX_SLABS = {
    "new_regime": [
        {"min": 0, "max": 400000, "rate": 0},
        {"min": 400000, "max": 800000, "rate": 0.05},
        {"min": 800000, "max": 1200000, "rate": 0.10},
        {"min": 1200000, "max": 1600000, "rate": 0.15},
        {"min": 1600000, "max": 2000000, "rate": 0.20},
        {"min": 2000000, "max": 2400000, "rate": 0.25},
        {"min": 2400000, "max": None, "rate": 0.30},
    ],
    "old_regime": [
        {"min": 0, "max": 250000, "rate": 0},
        {"min": 250000, "max": 500000, "rate": 0.05},
        {"min": 500000, "max": 1000000, "rate": 0.20},
        {"min": 1000000, "max": None, "rate": 0.30},
    ],
    "rebate_87A": {
        "new_regime": {"limit": 700000, "rebate": "Full tax rebate"},
        "old_regime": {"limit": 500000, "rebate": "₹12,500 max"},
    }
}

# SEBI Regulations for Investment Advisers
SEBI_REGULATIONS = {
    "registration": {
        "required": True,
        "qualifications": [
            "NISM Series XA and XB certification",
            "Or CFA/CFP/CA qualification",
            "5 years experience in financial services",
        ],
        "net_worth": {
            "individual": 5000000,  # ₹5 lakh
            "corporate": 20000000,  # ₹2 crore
        }
    },
    "disclosures": [
        "All fees and charges must be disclosed upfront",
        "Conflict of interest must be disclosed",
        "Risk disclosure mandatory",
        "Past performance disclaimer required",
    ],
    "prohibited": [
        "Guaranteeing returns",
        "Charging profit sharing without registration",
        "Providing tips without SEBI registration",
        "Making unsolicited calls",
    ]
}

# Important Court Judgments
COURT_JUDGMENTS = {
    "CIT v. Emirates Airlines": {
        "year": 2010,
        "issue": "HRA exemption for rented parent's house",
        "ruling": "Allowed if genuine transaction",
    },
    "CIT v. Baji Rani Kshyap": {
        "year": 2013,
        "issue": "Cash gifts from relatives",
        "ruling": "Not taxable if source explained",
    },
    "CIT v. Saurabh Jhunjhunwala": {
        "year": 2015,
        "issue": "Section 54F exemption",
        "ruling": "Can invest in multiple houses",
    },
    "CIT v. V. Raghuraman": {
        "year": 2019,
        "issue": "Indexation benefit on debt funds",
        "ruling": "Available only for LTCG (>36 months)",
    }
}

def get_tax_section_info(section: str) -> dict:
    """Get detailed information about a tax section"""
    return INCOME_TAX_SECTIONS.get(section, {"error": f"Section {section} not found"})

def get_capital_gains_info(asset_type: str, holding_period: str = None) -> dict:
    """Get capital gains tax information"""
    if asset_type not in CAPITAL_GAINS:
        return {"error": f"Asset type {asset_type} not supported"}
    
    info = CAPITAL_GAINS[asset_type]
    if holding_period:
        key = "LTCG" if holding_period in ["long", "ltcg", "12+"] else "STCG"
        return info.get(key, info)
    return info

def get_tax_slab(regime: str = "new") -> list:
    """Get tax slabs for given regime"""
    key = "new_regime" if regime == "new" else "old_regime"
    return TAX_SLABS[key]

def get_sebi_requirements() -> dict:
    """Get SEBI registration requirements"""
    return SEBI_REGULATIONS

def get_court_judgment(case_name: str = None) -> dict:
    """Get court judgment information"""
    if case_name:
        return COURT_JUDGMENTS.get(case_name, {"error": "Case not found"})
    return COURT_JUDGMENTS

def calculate_total_deductions(deductions: dict) -> dict:
    """Calculate total eligible deductions"""
    total = 0
    breakdown = {}
    
    # 80C
    if "section_80c" in deductions:
        breakdown["80C"] = min(deductions["section_80c"], 150000)
        total += breakdown["80C"]
    
    # 80CCD(1B) - NPS additional
    if "section_80ccd_1b" in deductions:
        breakdown["80CCD(1B)"] = min(deductions["section_80ccd_1b"], 50000)
        total += breakdown["80CCD(1B)"]
    
    # 80D - Health insurance
    if "section_80d" in deductions:
        breakdown["80D"] = min(deductions["section_80d"], 75000)
        total += breakdown["80D"]
    
    # 80E - Education loan interest
    if "section_80e" in deductions:
        breakdown["80E"] = deductions["section_80e"]
        total += breakdown["80E"]
    
    # 80TTA - Savings interest
    if "section_80tta" in deductions:
        breakdown["80TTA"] = min(deductions["section_80tta"], 10000)
        total += breakdown["80TTA"]
    
    return {
        "total_deductions": total,
        "breakdown": breakdown
    }
