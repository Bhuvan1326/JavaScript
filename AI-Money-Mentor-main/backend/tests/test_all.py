#!/usr/bin/env python3
"""
Comprehensive Test Suite for AI Money Mentor
End-to-end testing of all modules
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_niveshak():
    """Test MF Portfolio X-Ray"""
    print("\n" + "="*60)
    print("TESTING NIVESHAK (MF Portfolio X-Ray)")
    print("="*60)
    
    from agents.niveshak import PortfolioAnalyzer
    from agents.niveshak.mf_data import MFDataFetcher
    
    # Test 1: Portfolio Analyzer - XIRR Calculation
    print("\n[TEST 1] Portfolio Analyzer - XIRR Calculation")
    try:
        analyzer = PortfolioAnalyzer()
        
        # Sample transactions for XIRR test
        transactions = [
            {'date': '2022-01-01', 'amount': -10000, 'units': 100},
            {'date': '2022-07-01', 'amount': -10000, 'units': 95},
            {'date': '2023-01-01', 'amount': -10000, 'units': 90},
            {'date': '2024-01-01', 'amount': 35000, 'units': 0},  # Redemption
        ]
        
        # Calculate XIRR
        xirr = analyzer.calculate_xirr(transactions)
        print(f"  ✅ XIRR calculated: {xirr:.2f}%")
        assert -100 <= xirr <= 200, f"XIRR {xirr} out of expected range"
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Portfolio Metrics
    print("\n[TEST 2] Portfolio Analyzer - Risk Metrics")
    try:
        # Sample NAV data for Sharpe ratio
        nav_data = [100, 102, 101, 105, 108, 106, 110, 112, 111, 115]
        
        sharpe = analyzer.calculate_sharpe_ratio(nav_data, risk_free_rate=0.06)
        print(f"  ✅ Sharpe Ratio: {sharpe:.2f}")
        
        sortino = analyzer.calculate_sortino_ratio(nav_data, risk_free_rate=0.06)
        print(f"  ✅ Sortino Ratio: {sortino:.2f}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 3: MF Data Fetcher
    print("\n[TEST 3] MF Data Fetcher")
    try:
        fetcher = MFDataFetcher()
        print(f"  ✅ MFDataFetcher initialized")
        print(f"  ✅ Ready to fetch NAV data from mfapi.in")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("\n✅ NIVESHAK: ALL TESTS PASSED")
    return True


def test_karvid():
    """Test Tax Wizard"""
    print("\n" + "="*60)
    print("TESTING KARVID (Tax Wizard)")
    print("="*60)
    
    from agents.karvid import KarVidTaxCalculator, calculate_new_regime_tax, calculate_old_regime_tax
    
    # Test 1: New Tax Regime 2025-26
    print("\n[TEST 1] New Tax Regime Calculation")
    try:
        calc = KarVidTaxCalculator()
        
        # Income 12L - should be tax free under new regime with rebate
        result_12l = calculate_new_regime_tax(1200000)
        print(f"  ✅ Tax on ₹12L: ₹{result_12l['total_tax']:,.0f} (should be ~₹0 with rebate)")
        
        # Income 15L
        result_15l = calculate_new_regime_tax(1500000)
        print(f"  ✅ Tax on ₹15L: ₹{result_15l['total_tax']:,.0f}")
        
        # Income 24L
        result_24l = calculate_new_regime_tax(2400000)
        print(f"  ✅ Tax on ₹24L: ₹{result_24l['total_tax']:,.0f}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Old Tax Regime
    print("\n[TEST 2] Old Tax Regime Calculation")
    try:
        result_old_12l = calculate_old_regime_tax(1200000)
        print(f"  ✅ Old regime tax on ₹12L: ₹{result_old_12l['total_tax']:,.0f}")
        
        result_old_20l = calculate_old_regime_tax(2000000)
        print(f"  ✅ Old regime tax on ₹20L: ₹{result_old_20l['total_tax']:,.0f}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 3: Regime Comparison
    print("\n[TEST 3] Regime Comparison")
    try:
        from agents.karvid import compare_regimes
        
        income = 1500000
        result = compare_regimes(income)
        
        print(f"  ✅ Income: ₹{income:,.0f}")
        print(f"  ✅ New Regime Tax: ₹{result['new_regime']['total_tax']:,.0f}")
        print(f"  ✅ Old Regime Tax: ₹{result['old_regime']['total_tax']:,.0f}")
        print(f"  ✅ Recommended: {result['recommended_regime']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: 80C Deductions
    print("\n[TEST 4] 80C Deductions")
    try:
        from agents.karvid.deductions import calculate_80c_deduction
        
        deductions = {
            'ppf': 150000,
            'elss': 50000,
            'life_insurance_premium': 30000,
        }
        
        result = calculate_80c_deduction(**deductions)
        total_claimed = result.get("total_claimed", 0)
        eligible = result.get("allowed_deduction", 0)
        excess = max(0, total_claimed - eligible)
        print(f"  ✅ Total 80C claimed: ₹{total_claimed:,.0f}")
        print(f"  ✅ Eligible deduction: ₹{eligible:,.0f}")
        print(f"  ✅ Excess over limit: ₹{excess:,.0f}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 5: Capital Gains
    print("\n[TEST 5] Capital Gains Tax")
    try:
        from agents.karvid.capital_gains import calculate_equity_ltcg
        
        # LTCG on equity above ₹1.25L exemption
        result = calculate_equity_ltcg(sale_price=300000, purchase_price=100000, days_held=400)
        print(f"  ✅ LTCG on ₹2L gain: ₹{result.tax_amount:,.0f} tax")
        print(f"  ✅ Exemption used: ₹{result.exemption:,.0f}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("\n✅ KARVID: ALL TESTS PASSED")
    return True


def test_yojanakarta():
    """Test FIRE Planner"""
    print("\n" + "="*60)
    print("TESTING YOJANAKARTA (FIRE Planner)")
    print("="*60)
    
    from agents.yojana.fire_calculator import FIRECalculator, calculate_fire_number_india, get_sip_recommendation
    
    # Test 1: FIRE Number Calculation
    print("\n[TEST 1] FIRE Number Calculation")
    try:
        monthly_expenses = 50000
        
        fire_numbers = calculate_fire_number_india(monthly_expenses)
        
        print(f"  ✅ Monthly Expenses: ₹{monthly_expenses:,.0f}")
        print(f"  ✅ Classic FIRE (4%): ₹{fire_numbers['classic_fire']:,.0f}")
        print(f"  ✅ Conservative (3%): ₹{fire_numbers['conservative_fire']:,.0f}")
        print(f"  ✅ Fat FIRE: ₹{fire_numbers['fat_fire']:,.0f}")
        
        # Verify: FIRE number should be ~25x annual expenses for 4% rule
        expected = monthly_expenses * 12 / 0.04
        assert abs(fire_numbers['classic_fire'] - expected) < 1000, "FIRE number calculation mismatch"
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Years to FIRE
    print("\n[TEST 2] Years to FIRE Calculation")
    try:
        calc = FIRECalculator(
            monthly_expenses=50000,
            current_age=30,
            retirement_age=45,
            current_corpus=500000,
            expected_return=0.12
        )
        
        monthly_sip = calc.calculate_monthly_savings()
        print(f"  ✅ Monthly SIP needed for 15 years: ₹{monthly_sip:,.0f}")
        
        years = calc.calculate_years_to_fire(monthly_savings=50000)
        print(f"  ✅ Years to FIRE with ₹50k SIP: {years} years")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 3: SIP Roadmap
    print("\n[TEST 3] SIP Roadmap Generation")
    try:
        roadmap = calc.generate_sip_roadmap(years=5)
        
        print(f"  ✅ Roadmap generated for {len(roadmap)} years")
        print(f"  ✅ Year 1: Corpus ₹{roadmap[0]['corpus']:,.0f}, Progress {roadmap[0]['progress']:.1f}%")
        print(f"  ✅ Year 5: Corpus ₹{roadmap[4]['corpus']:,.0f}, Progress {roadmap[4]['progress']:.1f}%")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: SIP Recommendation
    print("\n[TEST 4] SIP for Target Corpus")
    try:
        sip_rec = get_sip_recommendation(target_corpus=10000000, years=15)
        
        print(f"  ✅ To reach ₹1Cr in 15 years:")
        print(f"  ✅ Monthly SIP: ₹{sip_rec['monthly_sip']:,.0f}")
        print(f"  ✅ Total Investment: ₹{sip_rec['total_investment']:,.0f}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("\n✅ YOJANAKARTA: ALL TESTS PASSED")
    return True


def test_bazaarguru():
    """Test Market Research"""
    print("\n" + "="*60)
    print("TESTING BAZAARGURU (Market Research)")
    print("="*60)
    
    from agents.bazaar.stock_data import StockData, StockQuote, MOCK_STOCKS
    
    # Test 1: Stock Data Initializer
    print("\n[TEST 1] Stock Data")
    try:
        sd = StockData()
        print(f"  ✅ StockData initialized")
        print(f"  ✅ MOCK_STOCKS length: {len(MOCK_STOCKS)} stocks")
        print(f"  ✅ NIFTY_50: {len(StockData.NIFTY_50)} stocks")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Stock Quote (Note: May fail without network)
    print("\n[TEST 2] Stock Quote Fetch")
    try:
        quote = sd.get_quote("RELIANCE")
        if quote:
            print(f"  ✅ RELIANCE: ₹{quote.price:,.2f} ({quote.change_percent:+.2f}%)")
        else:
            print(f"  ⚠️ Network not available, skipping live quote test")
    except Exception as e:
        print(f"  ⚠️ Network error (expected without internet): {e}")
    
    # Test 3: Market Overview
    print("\n[TEST 3] Market Overview")
    try:
        overview = sd.get_market_overview()
        print(f"  ✅ Market overview fetched")
        print(f"  ✅ Nifty value: {overview['nifty']['value']}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: Popular Stocks List
    print("\n[TEST 4] Popular Stocks")
    try:
        popular = list(MOCK_STOCKS.keys())[:5]
        print(f"  ✅ Top 5 Popular: {', '.join(popular)}")
        
        nifty_50_count = len(StockData.NIFTY_50)
        print(f"  ✅ NIFTY 50 stocks: {nifty_50_count}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("\n✅ BAZAARGURU: ALL TESTS PASSED")
    return True


def test_dhanraksha():
    """Test Financial Health Score"""
    print("\n" + "="*60)
    print("TESTING DHANRAKSHA (Financial Health Score)")
    print("="*60)
    
    from agents.dhan.health_score import FinancialHealthCalculator, get_health_score
    
    # Test 1: Basic Health Score Calculation
    print("\n[TEST 1] Health Score Calculation")
    try:
        calc = FinancialHealthCalculator(
            monthly_income=100000,
            monthly_expenses=50000,
            monthly_emi=10000,
            monthly_savings=20000,
            monthly_investments=15000,
            emergency_fund=300000,
            life_insurance_cover=5000000,
            health_insurance_cover=500000,
            retirement_corpus=1000000,
            age=30,
            credit_score=750,
            dependents=2
        )
        
        report = calc.calculate_overall_score()
        
        print(f"  ✅ Overall Score: {report.overall_score:.0f}/100")
        print(f"  ✅ Grade: {report.grade}")
        print(f"  ✅ Financial Age: {report.financial_age}")
        print(f"  ✅ Monthly Surplus: ₹{report.monthly_surplus:,.0f}")
        
        assert 0 <= report.overall_score <= 100, "Score out of range"
        assert report.grade in ['A+', 'A', 'B', 'C', 'D', 'F'], "Invalid grade"
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 2: Individual Metrics
    print("\n[TEST 2] Individual Health Metrics")
    try:
        metrics = report.metrics
        
        for metric in metrics:
            status_emoji = "✅" if metric.status in ['excellent', 'good'] else "⚠️"
            print(f"  {status_emoji} {metric.category}: {metric.score:.0f} - {metric.message}")
        
        # Verify all 8 metrics present
        assert len(metrics) == 8, f"Expected 8 metrics, got {len(metrics)}"
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 3: Convenience Function
    print("\n[TEST 3] Convenience Function")
    try:
        result = get_health_score(
            monthly_income=100000,
            monthly_expenses=50000
        )
        
        print(f"  ✅ Quick score: {result['overall_score']:.0f}")
        print(f"  ✅ Grade: {result['grade']}")
        print(f"  ✅ Metrics: {len(result['metrics'])} factors")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    # Test 4: Edge Cases
    print("\n[TEST 4] Edge Cases")
    try:
        # Zero income
        calc_zero = FinancialHealthCalculator(monthly_income=0, monthly_expenses=50000)
        report_zero = calc_zero.calculate_overall_score()
        print(f"  ✅ Zero income handled: score {report_zero.overall_score:.0f}")
        
        # High income, low expenses
        calc_high = FinancialHealthCalculator(
            monthly_income=500000,
            monthly_expenses=100000,
            monthly_savings=100000,
            monthly_investments=200000
        )
        report_high = calc_high.calculate_overall_score()
        print(f"  ✅ High income scenario: score {report_high.overall_score:.0f}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False
    
    print("\n✅ DHANRAKSHA: ALL TESTS PASSED")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 AI MONEY MENTOR - END-TO-END TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Run each test module
    results['niveshak'] = test_niveshak()
    results['karvid'] = test_karvid()
    results['yojanakarta'] = test_yojanakarta()
    results['bazaarguru'] = test_bazaarguru()
    results['dhanraksha'] = test_dhanraksha()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for module, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {module.upper()}: {status}")
    
    print(f"\n{passed}/{total} test suites passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️ SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
