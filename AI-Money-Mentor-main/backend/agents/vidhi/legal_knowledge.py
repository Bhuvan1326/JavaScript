"""
Vidhi - Legal Knowledge Base
Indian Constitution, SEBI, RBI, and Financial Laws
"""

# Constitution of India - Economic Provisions
CONSTITUTION_PROVISIONS = {
    "Article_265": {
        "title": "No tax without authority of law",
        "text": "No tax shall be levied or collected except by authority of law",
        "implication": "Every tax must have legislative backing",
    },
    "Article_266": {
        "title": "Consolidated Funds",
        "text": "All taxes form part of Consolidated Fund of India",
        "implication": "Government must account for all tax revenue",
    },
    "Article_267": {
        "title": "Contingency Fund",
        "text": "Parliament can create Contingency Fund",
        "implication": "Emergency expenditures possible",
    },
    "Article_269": {
        "title": "Taxes levied by Union but collected by States",
        "text": "Stamp duties, excise on medicinal preparations",
        "implication": "Federal structure of taxation",
    },
    "Article_270": {
        "title": "Taxes levied and collected by Union and distributed",
        "text": "Income tax, Union excise duties distributed to States",
        "implication": "Central taxes shared with States",
    },
    "Article_276": {
        "title": "Taxes on professions, trades, etc.",
        "text": "States can levy profession tax up to ₹2,500/year",
        "implication": "Professional tax ceiling",
    },
    "Article_300A": {
        "title": "Right to Property",
        "text": "No person shall be deprived of property save by authority of law",
        "implication": "Property rights protected but not fundamental",
    },
    "Article_366": {
        "title": "Definitions",
        "text": "Defines 'tax', 'duty', 'cess', 'fee'",
        "implication": "Legal definitions for taxation",
    }
}

# Income Tax Act, 1961 - Key Sections
INCOME_TAX_ACT = {
    "Section_1": "Short title and extent",
    "Section_2": "Definitions (includes 'income', 'person', 'assessee')",
    "Section_3": "Previous year",
    "Section_4": "Charge of income tax",
    "Section_5": "Scope of total income",
    "Section_5A": "Apportionment of income",
    "Section_6": "Residence in India",
    "Section_7": "Income deemed to accrue or arise in India",
    "Section_8": "Dividend income",
    "Section_9": "Income deemed to accrue or arise in India",
    "Section_10": "Incomes not included in total income",
    "Section_14": "Heads of income",
    "Section_15": "Salaries",
    "Section_16": "Deductions from salaries",
    "Section_17": "Salary perquisites",
    "Section_22": "Income from house property",
    "Section_23": "Annual value of house property",
    "Section_24": "Deductions from house property",
    "Section_28": "Profits and gains of business",
    "Section_29": "Deductions from business income",
    "Section_44AD": "Presumptive taxation for small businesses",
    "Section_44ADA": "Presumptive taxation for professionals",
    "Section_44AE": "Presumptive taxation for truck operators",
    "Section_45": "Capital gains charge",
    "Section_48": "Computation of capital gains",
    "Section_54": "Exemption on sale of house property",
    "Section_54EC": "Exemption on investment in bonds",
    "Section_54F": "Exemption on sale of capital asset",
    "Section_56": "Income from other sources",
    "Section_68": "Cash credits",
    "Section_69": "Unexplained investments",
    "Section_69A": "Unexplained money",
    "Section_69B": "Investment not recorded in books",
    "Section_69C": "Unexplained expenditure",
    "Section_69D": "Amount borrowed/repaid on hundi",
    "Section_80C": "Deductions for savings (up to ₹1.5 lakh)",
    "Section_80D": "Health insurance premium",
    "Section_80CCD": "NPS contributions",
    "Section_80TTA": "Interest on savings account",
    "Section_139": "Return of income",
    "Section_140A": "Self-assessment and payment",
    "Section_143": "Assessment",
    "Section_148": "Reassessment",
    "Section_154": "Rectification of mistakes",
    "Section_220": "Interest payable by assessee",
    "Section_234A": "Interest for default in furnishing return",
    "Section_234B": "Interest for default in advance tax",
    "Section_234C": "Interest for deferment of advance tax",
    "Section_234E": "Interest for default in TDS/TCS returns",
    "Section_234F": "Late filing fee",
    "Section_271": "Penalties",
    "Section_276C": "Prosecution for willful attempt to evade tax",
}

# SEBI Regulations
SEBI_ACTS = {
    "SEBI_Act_1992": {
        "full_name": "Securities and Exchange Board of India Act, 1992",
        "purpose": "Establish SEBI and protect investor interests",
        "key_sections": {
            "Section_11": "Functions of SEBI",
            "Section_11A": "Powers of SEBI",
            "Section_11B": "SEBI's power to issue directions",
            "Section_12": "Registration of intermediaries",
            "Section_24": "Power to impose penalty",
        }
    },
    "SEBI_Investment_Advisers_2013": {
        "full_name": "SEBI (Investment Advisers) Regulations, 2013",
        "applicability": "All persons providing investment advice",
        "requirements": {
            "Registration": "Mandatory with SEBI",
            "Qualification": "NISM XA + XB or CFA/CFP/CA",
            "Experience": "5 years in financial services",
            "Net Worth": "₹5 lakh (individual), ₹2 crore (corporate)",
            "Compliance_Officer": "Mandatory for corporate",
            "Conflict_of_Interest": "Must disclose",
            "Risk_Disclosure": "Mandatory for all advice",
        },
        "prohibited_activities": [
            "Guaranteeing returns",
            "Charging profit-sharing (without registration)",
            "Providing tips without research",
            "Unsolicited calls/messages",
        ]
    },
    "SEBI_Portfolio_Managers_2020": {
        "full_name": "SEBI (Portfolio Managers) Regulations, 2020",
        "minimum_investment": "₹1 crore",
        "disclosures": [
            "Investment strategy",
            "Risk factors",
            "Fee structure",
            "Performance track record",
        ]
    },
    "SEBI_Mutual_Funds_1996": {
        "full_name": "SEBI (Mutual Funds) Regulations, 1996",
        "key_requirements": {
            "Offer_Document": "Mandatory with riskometer",
            "NAV_Disclosure": "Daily disclosure",
            "Expense_Ratio": "Maximum limits prescribed",
            "Exit_Load": "Must be disclosed",
        }
    },
    "SEBI_Research_Analysts_2014": {
        "full_name": "SEBI (Research Analysts) Regulations, 2014",
        "applicability": "All persons providing research reports",
        "requirements": [
            "Registration with SEBI",
            "Conflict of interest disclosure",
            "Rating methodology disclosure",
            "Compensation disclosure",
        ]
    }
}

# RBI Regulations
RBI_REGULATIONS = {
    "Banking_Regulation_Act_1949": {
        "purpose": "Regulate banking companies",
        "key_sections": {
            "Section_10": "Board of Directors",
            "Section_11": "Paid-up capital",
            "Section_12": "Reserve fund",
            "Section_18": "Cash reserve",
        }
    },
    "RBI_Act_1934": {
        "purpose": "Establish Reserve Bank of India",
        "key_sections": {
            "Section_21": "Bank receives and makes payments",
            "Section_22": "Issue of bank notes",
            "Section_26": "Legal tender",
        }
    },
    "FEMA_1999": {
        "full_name": "Foreign Exchange Management Act, 1999",
        "purpose": "Regulate foreign exchange transactions",
        "key_points": [
            "All forex transactions must be through authorized dealers",
            "LRS limit: $250,000/year per person",
            "FPI investment limits prescribed",
            "Reporting requirements for foreign investments",
        ]
    },
    "PMLA_2002": {
        "full_name": "Prevention of Money Laundering Act, 2002",
        "purpose": "Prevent money laundering",
        "key_requirements": [
            "KYC mandatory for all financial transactions",
            "CTR: Cash transactions > ₹10 lakh",
            "STR: Suspicious transactions must be reported",
            "PEP: Enhanced due diligence for Politically Exposed Persons",
        ]
    }
}

# Consumer Protection Act, 2019
CONSUMER_PROTECTION = {
    "Consumer_Rights": [
        "Right to safety",
        "Right to be informed",
        "Right to choose",
        "Right to be heard",
        "Right to seek redressal",
        "Right to consumer education",
    ],
    "E_Commerce_Rules_2020": {
        "disclosures": [
            "Seller details",
            "Product specifications",
            "Price breakup",
            "Return policy",
            "Warranty information",
        ],
        "prohibited": [
            "Unfair trade practices",
            "Hidden charges",
            "False reviews",
            "Flash sales without inventory",
        ]
    }
}

def get_constitution_provision(article: str) -> dict:
    """Get Constitution provision"""
    key = f"Article_{article}" if not article.startswith("Article") else article
    return CONSTITUTION_PROVISIONS.get(key, {"error": f"Article not found"})

def get_income_tax_section(section: str) -> str:
    """Get Income Tax Act section description"""
    key = f"Section_{section}" if not section.startswith("Section") else section
    return INCOME_TAX_ACT.get(key, f"Section {section} not found")

def get_sebi_regulation(name: str = None) -> dict:
    """Get SEBI regulation details"""
    if name:
        return SEBI_ACTS.get(name, {"error": "Regulation not found"})
    return SEBI_ACTS

def get_rbi_regulation(name: str = None) -> dict:
    """Get RBI regulation details"""
    if name:
        return RBI_REGULATIONS.get(name, {"error": "Regulation not found"})
    return RBI_REGULATIONS

def get_consumer_protection() -> dict:
    """Get Consumer Protection Act details"""
    return CONSUMER_PROTECTION

def get_legal_disclaimer() -> str:
    """Get legal disclaimer for financial advice"""
    return """
IMPORTANT LEGAL DISCLAIMER

This platform provides educational information only. It is NOT:
- A SEBI-registered investment advisor
- Authorized to give specific investment advice
- Liable for any financial decisions made based on this information

SEBI (Investment Advisers) Regulations, 2013 require:
- Registration for providing investment advice
- Risk disclosure before any recommendation
- Conflict of interest disclosure

Income Tax Act, 1961:
- Tax calculations are estimates based on current laws
- Individual situations may vary
- Consult a tax professional for specific advice

Constitution of India (Article 265):
- No tax shall be levied except by authority of law
- All tax advice must cite relevant sections

For personalized advice, please consult:
- A SEBI-registered investment adviser for investments
- A practicing Chartered Accountant for tax matters
- A qualified lawyer for legal matters
"""
