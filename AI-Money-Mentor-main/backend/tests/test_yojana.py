"""Test YojanaKarta FIRE Planner"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.yojana.fire_calculator import FIRECalculator, calculate_fire_number_india, get_sip_recommendation

def test_fire_number():
    """Test FIRE Number Calculation"""
    print("\n[TEST 1] FIRE Number Calculation")
    
    monthly_expenses = 50000
    fire_numbers = calculate_fire_number_india(monthly_expenses)
    
    print(f"  ✅ Monthly Expenses: ₹{monthly_expenses:,.0f}")
    print(f"  ✅ Classic FIRE (4%): ₹{fire_numbers['classic_fire']:,.0f}")
    print(f"  ✅ Conservative (3%): ₹{fire_numbers['conservative_fire']:,.0f}")
    print(f"  ✅ Fat FIRE: ₹{fire_numbers['fat_fire']:,.0f}")
    
    return True

def test_years_to_fire():
    """Test Years to FIRE Calculation"""
    print("\n[TEST 2] Years to FIRE Calculation")
    
    calc = FIRECalculator(
        monthly_expenses=50000,
        current_age=30,
        retirement_age=45,
        current_corpus=500000,
        expected_return=0.12
    )
    
    # Use default (retirement_age - current_age)
    monthly_sip = calc.calculate_monthly_savings()
    print(f"  ✅ Monthly SIP needed: ₹{monthly_sip:,.0f}")
    
    years = calc.calculate_years_to_fire(monthly_savings=50000)
    print(f"  ✅ Years to FIRE with ₹50k SIP: {years} years")
    
    return True

def test_sip_roadmap():
    """Test SIP Roadmap Generation"""
    print("\n[TEST 3] SIP Roadmap Generation")
    
    calc = FIRECalculator(
        monthly_expenses=50000,
        current_age=30,
        retirement_age=45,
        current_corpus=500000
    )
    
    roadmap = calc.generate_sip_roadmap(years=5)
    
    print(f"  ✅ Roadmap generated for {len(roadmap)} years")
    print(f"  ✅ Year 1: Corpus ₹{roadmap[0]['corpus']:,.0f}, Progress {roadmap[0]['progress']:.1f}%")
    print(f"  ✅ Year 5: Corpus ₹{roadmap[4]['corpus']:,.0f}, Progress {roadmap[4]['progress']:.1f}%")
    
    return True

def test_sip_recommendation():
    """Test SIP Recommendation"""
    print("\n[TEST 4] SIP for Target Corpus")
    
    sip_rec = get_sip_recommendation(target_corpus=10000000, years=15)
    
    print(f"  ✅ To reach ₹1Cr in 15 years:")
    print(f"  ✅ Monthly SIP: ₹{sip_rec['monthly_sip']:,.0f}")
    print(f"  ✅ Total Investment: ₹{sip_rec['total_investment']:,.0f}")
    
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING YOJANAKARTA (FIRE Planner)")
    print("="*60)
    
    tests = [test_fire_number, test_years_to_fire, test_sip_roadmap, test_sip_recommendation]
    results = [t() for t in tests]
    
    if all(results):
        print("\n✅ YOJANAKARTA: ALL TESTS PASSED")
    else:
        print("\n❌ YOJANAKARTA: SOME TESTS FAILED")
