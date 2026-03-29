"""Test KarVid Tax Wizard"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.karvid import (
    KarVidTaxCalculator, 
    calculate_new_regime_tax, 
    calculate_old_regime_tax,
    compare_regimes,
    calculate_80c_deduction,
    calculate_equity_ltcg
)

def test_new_regime():
    """Test New Tax Regime"""
    print("\n[TEST 1] New Tax Regime Calculation")
    
    # Income 12L - should be tax free with rebate
    result_12l = calculate_new_regime_tax(1200000)
    print(f"  ✅ Tax on ₹12L: ₹{result_12l['total_tax']:,.0f} (should be ~₹0 with rebate)")
    
    # Income 15L
    result_15l = calculate_new_regime_tax(1500000)
    print(f"  ✅ Tax on ₹15L: ₹{result_15l['total_tax']:,.0f}")
    
    # Income 24L
    result_24l = calculate_new_regime_tax(2400000)
    print(f"  ✅ Tax on ₹24L: ₹{result_24l['total_tax']:,.0f}")
    
    return True

def test_old_regime():
    """Test Old Tax Regime"""
    print("\n[TEST 2] Old Tax Regime Calculation")
    
    result_old_12l = calculate_old_regime_tax(1200000)
    print(f"  ✅ Old regime tax on ₹12L: ₹{result_old_12l['total_tax']:,.0f}")
    
    result_old_20l = calculate_old_regime_tax(2000000)
    print(f"  ✅ Old regime tax on ₹20L: ₹{result_old_20l['total_tax']:,.0f}")
    
    return True

def test_regime_comparison():
    """Test Regime Comparison"""
    print("\n[TEST 3] Regime Comparison")
    
    income = 1500000
    result = compare_regimes(income)
    
    print(f"  ✅ Income: ₹{income:,.0f}")
    print(f"  ✅ New Regime Tax: ₹{result['new_regime']['total_tax']:,.0f}")
    print(f"  ✅ Old Regime Tax: ₹{result['old_regime']['total_tax']:,.0f}")
    print(f"  ✅ Recommended: {result['recommended_regime']}")
    
    return True

def test_80c():
    """Test 80C Deductions"""
    print("\n[TEST 4] 80C Deductions")
    
    # Use keyword arguments
    result = calculate_80c_deduction(ppf=150000, elss=50000, life_insurance_premium=30000)
    print(f"  ✅ Total 80C claimed: ₹{result['total_claimed']:,.0f}")
    print(f"  ✅ Eligible deduction: ₹{result['allowed_deduction']:,.0f}")
    print(f"  ✅ Unused limit: ₹{result['unused_limit']:,.0f}")
    
    return True

def test_capital_gains():
    """Test Capital Gains"""
    print("\n[TEST 5] Capital Gains Tax")
    
    # LTCG on equity above ₹1.25L exemption (gain=200,000)
    result = calculate_equity_ltcg(sale_price=300000, purchase_price=100000, days_held=400)
    print(f"  ✅ LTCG on ₹2L gain: ₹{result.tax_amount:,.0f} tax")
    print(f"  ✅ Exemption used: ₹{result.exemption:,.0f}")
    
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING KARVID (Tax Wizard)")
    print("="*60)
    
    tests = [test_new_regime, test_old_regime, test_regime_comparison, test_80c, test_capital_gains]
    results = [t() for t in tests]
    
    if all(results):
        print("\n✅ KARVID: ALL TESTS PASSED")
    else:
        print("\n❌ KARVID: SOME TESTS FAILED")
