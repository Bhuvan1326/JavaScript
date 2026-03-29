# KarVid Agent - Indian Tax Calculator

**Part of AI Money Mentor - ET GenAI Hackathon 2026**

KarVid (कर-Vid = Tax Knowledge) is a specialized agent for Indian Income Tax calculations, focusing on FY 2025-26 (AY 2026-27).

## 📁 Files Overview

### 1. `tax_brackets.py`
Income tax slabs for both regimes.

**Key Features:**
- New Tax Regime slabs (0-4L: Nil, 4-8L: 5%, 8-12L: 10%, 12-16L: 15%, 16-20L: 20%, 20-24L: 25%, 24L+: 30%)
- Old Tax Regime slabs (0-2.5L: Nil, 2.5-5L: 5%, 5-10L: 20%, 10L+: 30%)
- Section 87A rebate calculation (₹60,000 New / ₹12,500 Old)
- Standard deduction (₹75,000 New / ₹50,000 Old)
- Surcharge calculations for high income

```python
from tax_brackets import calculate_new_regime_tax, compare_regimes

result = calculate_new_regime_tax(income=1500000, is_salaried=True)
print(f"Tax: ₹{result['total_tax']:,.0f}")  # Tax: ₹97,500
```

### 2. `deductions.py`
All major deductions and exemptions.

**Key Features:**
- Section 80C (Investments: PPF, EPF, ELSS, etc.) - Max ₹1.5L
- Section 80D (Health Insurance) - Max ₹1L
- HRA Exemption calculation
- Section 80CCD (NPS) - Additional ₹50K
- Section 80E (Education Loan Interest) - No limit
- Home Loan Interest (24(b)) - Max ₹2L

```python
from deductions import calculate_80c_deduction, calculate_hra_exemption

result = calculate_80c_deduction(ppf=100000, elss=50000)
print(f"80C Deduction: ₹{result['allowed_deduction']:,.0f}")  # ₹150,000

hra = calculate_hra_exemption(hra_received=120000, basic_salary=600000, rent_paid=180000, metro_city=True)
print(f"HRA Exemption: ₹{hra['hra_exemption']:,.0f}")
```

### 3. `capital_gains.py`
Capital gains tax for all asset types.

**Key Features:**
- Equity LTCG: 12.5% (₹1.25L exemption)
- Equity STCG: 20%
- Debt Mutual Funds: At slab rate (post-Apr 2023)
- Real Estate: 12.5% without indexation (or 20% with indexation for old properties)
- Unlisted Shares: 12.5% (LTCG) or slab rate (STCG)
- Section 54/54F/54EC exemptions

```python
from capital_gains import calculate_capital_gains

result = calculate_capital_gains(
    asset_type="equity",
    sale_price=500000,
    purchase_price=300000,
    days_held=500,
    stt_paid=True
)
print(f"Tax: ₹{result.total_tax:,.0f}")  # Tax: ₹9,750
```

### 4. `tax_calculator.py`
Main calculator integrating all modules.

**Key Features:**
- Complete tax profile handling
- Regime comparison (New vs Old)
- Tax saving recommendations
- Comprehensive tax report generation
- Break-even deduction calculation

```python
from tax_calculator import KarVidTaxCalculator, TaxpayerProfile

profile = TaxpayerProfile(
    name="Sample",
    age=32,
    salary_income=1500000,
    ppf=100000,
    health_insurance_self=20000,
)
calculator = KarVidTaxCalculator(profile)
print(calculator.generate_tax_report())
```

## 🚀 Quick Start

```python
# Quick tax estimate
from tax_calculator import quick_tax_estimate

result = quick_tax_estimate(income=1500000, regime="new")
print(f"Tax: ₹{result['total_tax']:,.0f}")  # Tax: ₹97,500
print(f"Effective Rate: {result['effective_rate']}%")  # 6.5%
```

## 📊 Tax Summary FY 2025-26

### New Tax Regime (Default)
| Income Range | Tax Rate |
|--------------|----------|
| ₹0 - ₹4L | Nil |
| ₹4L - ₹8L | 5% |
| ₹8L - ₹12L | 10% |
| ₹12L - ₹16L | 15% |
| ₹16L - ₹20L | 20% |
| ₹20L - ₹24L | 25% |
| Above ₹24L | 30% |

**Benefits:**
- Standard Deduction: ₹75,000
- 87A Rebate: Up to ₹60,000 (zero tax up to ₹12L)
- Limited deductions available

### Old Tax Regime
| Income Range | Tax Rate |
|--------------|----------|
| ₹0 - ₹2.5L | Nil |
| ₹2.5L - ₹5L | 5% |
| ₹5L - ₹10L | 20% |
| Above ₹10L | 30% |

**Benefits:**
- All 70+ deductions and exemptions
- HRA, LTA exemptions
- 80C, 80D, 80CCD, etc.

## ⚠️ Important Notes

1. **Section 87A Rebate**: NOT applicable on capital gains (STCG/LTCG)
2. **STCG on Equity**: 20% special rate (not at slab)
3. **LTCG on Equity**: 12.5% with ₹1.25L exemption
4. **Debt MF**: Acquired post Apr 2023 - taxed at slab (no LTCG benefit)
5. **Real Estate**: 12.5% without indexation (post-July 2024)

## 📞 Support

For tax planning assistance, consult a qualified tax professional. This calculator provides estimates based on FY 2025-26 rules.

---

**KarVid Agent - AI Money Mentor**
*Empowering Indians with tax knowledge*
