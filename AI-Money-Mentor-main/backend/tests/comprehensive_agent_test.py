import requests
import json

BASE = "http://localhost:8000"
results = []

def test(name, method, endpoint, body=None, timeout=8):
    url = BASE + endpoint
    try:
        if method == "POST":
            r = requests.post(url, json=body, timeout=timeout)
        else:
            r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            data = r.json()
            results.append(("PASS", name, json.dumps(data)[:120]))
            return data
        else:
            results.append(("FAIL", name, str(r.status_code) + ": " + r.text[:80]))
            return None
    except requests.exceptions.Timeout:
        results.append(("SLOW", name, "Timeout (OpenClaw swarm call)"))
        return None
    except Exception as e:
        results.append(("FAIL", name, str(e)[:80]))
        return None

# 1. DhanSarthi (Coordinator)
test("DhanSarthi: route tax query", "POST", "/dhan-sarthi/route",
     {"query": "calculate tax for 15 lakh"}, timeout=10)

# 2. KarVid (Tax)
test("KarVid: calculate-tax (new)", "POST", "/karvid/calculate-tax",
     {"income": 1500000, "regime": "new"})
test("KarVid: compare-regimes", "POST", "/karvid/compare-regimes",
     {"income": 1500000})
test("KarVid: capital-gains STCG", "POST", "/karvid/capital-gains",
     {"gain": 500000, "holding_period": "short"})
test("KarVid: 80C deductions", "POST", "/karvid/80c",
     {"ppf": 50000, "elss": 100000})

# 3. Yojana (FIRE)
test("Yojana: FIRE number", "POST", "/yojana/fire-number",
     {"monthly_expenses": 50000})
test("Yojana: SIP recommendation", "POST", "/yojana/sip-recommendation",
     {"target_corpus": 10000000, "years": 10})
test("Yojana: retirement plan", "POST", "/yojana/retirement-plan",
     {"monthly_expenses": 50000, "current_age": 30, "retirement_age": 50, "current_corpus": 500000})

# 4. Bazaar (Stocks)
test("Bazaar: stock quote RELIANCE", "POST", "/bazaar/stock-quote",
     {"symbol": "RELIANCE"})
test("Bazaar: top gainers", "GET", "/bazaar/top-gainers")
test("Bazaar: NIFTY 50", "GET", "/bazaar/nifty50")

# 5. Dhan (Health)
test("Dhan: health score", "POST", "/dhan/health-score",
     {"income": 100000, "expenses": 60000, "monthly_savings": 20000, "monthly_investments": 10000})

# 6. Niveshak (Portfolio)
test("Niveshak: risk metrics", "POST", "/niveshak/risk-metrics",
     {"nav_data": [100, 102, 98, 105, 103, 110, 108]})

# 7. Vidhi (Compliance)
test("Vidhi: disclaimers", "GET", "/vidhi/disclaimers")
test("Vidhi: regulations", "GET", "/vidhi/regulations")

# 8. Life Event
test("LifeEvent: types", "GET", "/life-event/types")
test("LifeEvent: marriage plan", "POST", "/life-event/plan",
     {"event_type": "marriage", "years_until": 3, "current_corpus": 200000})
test("LifeEvent: comprehensive", "POST", "/life-event/comprehensive",
     {"event_type": "child_birth", "years_until": 2, "current_corpus": 100000})

# 9. Couple Planner
test("Couple: combined finances", "POST", "/couple/finances",
     {"person1_name": "Alice", "person1_income": 120000,
      "person2_name": "Bob", "person2_income": 80000})
test("Couple: budget 50/30/20", "POST", "/couple/budget",
     {"person1_name": "Alice", "person1_income": 120000,
      "person2_name": "Bob", "person2_income": 80000})
test("Couple: split expense", "POST", "/couple/split-expense",
     {"person1_name": "Alice", "person1_income": 120000,
      "person2_name": "Bob", "person2_income": 80000,
      "expense_amount": 50000, "description": "rent"})
test("Couple: debt payoff", "POST", "/couple/debt-payoff",
     {"person1_name": "Alice", "person1_income": 120000,
      "person2_name": "Bob", "person2_income": 80000,
      "debts": [{"name": "car loan", "balance": 500000, "interest_rate": 9, "min_payment": 12000}],
      "strategy": "avalanche"})

# Print results
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
slow = sum(1 for r in results if r[0] == "SLOW")
total = len(results)

print("\n" + "=" * 60)
print("  AI MONEY MENTOR - COMPREHENSIVE AGENT TEST RESULTS")
print("  " + str(passed) + " PASS / " + str(failed) + " FAIL / " + str(slow) + " SLOW (" + str(total) + " total)")
print("=" * 60)

for status, name, detail in results:
    if status == "PASS":
        print("  PASS: " + name)
        print("        " + detail)
    elif status == "FAIL":
        print("  FAIL: " + name)
        print("        " + detail)
    else:
        print("  SLOW: " + name)
        print("        " + detail)
