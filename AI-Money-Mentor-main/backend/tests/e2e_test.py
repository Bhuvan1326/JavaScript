import requests, json, sys

BASE = "http://localhost:8000"
passed = 0
failed = 0

def test(name, method, url, body=None):
    global passed, failed
    try:
        if method == "GET":
            r = requests.get(url, timeout=5)
        else:
            r = requests.post(url, json=body, timeout=5)
        if r.status_code == 200:
            print(f"  PASS: {name} -> {r.status_code}")
            passed += 1
        else:
            print(f"  FAIL: {name} -> {r.status_code} {r.text[:100]}")
            failed += 1
    except Exception as e:
        print(f"  FAIL: {name} -> {e}")
        failed += 1

print("=== E2E API TESTS ===")

test("Health Check", "GET", f"{BASE}/health")
test("Root Info", "GET", f"{BASE}/")

# Original agents
test("KarVid Tax", "POST", f"{BASE}/karvid/calculate-tax", {"income": 1500000, "regime": "new"})
test("KarVid Compare", "POST", f"{BASE}/karvid/compare-regimes", {"income": 1500000})
test("Yojana FIRE", "POST", f"{BASE}/yojana/fire-number", {"monthly_expenses": 50000, "current_age": 30})
test("Bazaar Stock", "POST", f"{BASE}/bazaar/stock-quote", {"symbol": "RELIANCE"})
test("Dhan Health", "POST", f"{BASE}/dhan/health-score", {"income": 100000, "expenses": 60000, "monthly_savings": 20000, "monthly_investments": 10000})
test("Vidhi Disclaimers", "GET", f"{BASE}/vidhi/disclaimers")
test("DhanSarthi Route", "POST", f"{BASE}/dhan-sarthi/route", {"query": "calculate my tax"})

# NEW agents
test("Life Event Types", "GET", f"{BASE}/life-event/types")
test("Life Event Plan", "POST", f"{BASE}/life-event/plan", {"event_type": "marriage", "years_until": 5, "current_corpus": 100000, "monthly_investment": 5000})
test("Life Event Comprehensive", "POST", f"{BASE}/life-event/comprehensive", {"age": 25, "income": 100000})
test("Couple Finances", "POST", f"{BASE}/couple/finances", {"person1_name": "Alice", "person1_income": 120000, "person2_name": "Bob", "person2_income": 80000})
test("Couple Plan", "POST", f"{BASE}/couple/plan", {"person1_name": "Alice", "person1_income": 120000, "person2_name": "Bob", "person2_income": 80000})
test("Couple Budget", "POST", f"{BASE}/couple/budget", {"person1_name": "Alice", "person1_income": 120000, "person2_name": "Bob", "person2_income": 80000})
test("Couple Split", "POST", f"{BASE}/couple/split-expense", {"person1_name": "Alice", "person1_income": 120000, "person2_name": "Bob", "person2_income": 80000, "expense_amount": 50000})

print(f"\n=== RESULTS: {passed} passed, {failed} failed ===")
sys.exit(1 if failed else 0)
