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
        results.append(("SLOW", name, "Timeout"))
        return None
    except Exception as e:
        results.append(("FAIL", name, str(e)[:80]))
        return None

# ==========================================
# PART 1: DHANSARTHI ROUTING VERIFICATION
# ==========================================
print("=" * 60)
print("  PART 1: DHANSARTHI SWARM ROUTING")
print("=" * 60)

routing_tests = [
    ("Tax calc query", {"query": "calculate my income tax for 15 lakh salary"}, "karvid"),
    ("Tax regime query", {"query": "should I choose old or new tax regime"}, "karvid"),
    ("Stock price query", {"query": "what is TCS share price today"}, "bazaar"),
    ("FIRE query", {"query": "how much do I need to retire early at 45"}, "yojana"),
    ("Health score query", {"query": "check my financial health"}, "dhan"),
    ("MF portfolio query", {"query": "analyze my mutual fund portfolio returns"}, "niveshak"),
    ("Legal compliance", {"query": "what are SEBI regulations for mutual funds"}, "vidhi"),
    ("Marriage planning", {"query": "I am getting married next year, help me plan finances"}, "life-event"),
    ("Couple finance", {"query": "me and my wife want to plan our joint budget"}, "couple-planner"),
]

for name, body, expected_agent in routing_tests:
    d = test("Route: " + name, "POST", "/dhan-sarthi/route", body, timeout=10)
    if d:
        actual = d.get("primary_agent", "unknown")
        if actual == expected_agent:
            print("  OK: '" + name + "' -> " + actual + " (correct)")
        else:
            print("  MISMATCH: '" + name + "' -> " + actual + " (expected " + expected_agent + ")")

# ==========================================
# PART 2: INDIVIDUAL AGENT DEEP TESTS
# ==========================================
print("\n" + "=" * 60)
print("  PART 2: INDIVIDUAL AGENT DEEP TESTS")
print("=" * 60)

# KarVid edge cases
print("\n--- KarVid (Tax) ---")
test("KarVid: 0 income", "POST", "/karvid/calculate-tax", {"income": 0, "regime": "new"})
test("KarVid: high income 50L", "POST", "/karvid/calculate-tax", {"income": 5000000, "regime": "old"})
test("KarVid: LTCG gains", "POST", "/karvid/capital-gains", {"gain": 200000, "holding_period": "long"})
test("KarVid: max 80C", "POST", "/karvid/80c", {"ppf": 150000, "elss": 50000, "lic": 20000})

# Yojana edge cases
print("\n--- Yojana (FIRE) ---")
test("Yojana: zero expenses FIRE", "POST", "/yojana/fire-number", {"monthly_expenses": 0})
test("Yojana: high expenses 2L", "POST", "/yojana/fire-number", {"monthly_expenses": 200000})
test("Yojana: SIP short 3yr", "POST", "/yojana/sip-recommendation", {"target_corpus": 5000000, "years": 3})
test("Yojana: retire young 25-40", "POST", "/yojana/retirement-plan",
     {"monthly_expenses": 40000, "current_age": 25, "retirement_age": 40, "current_corpus": 100000})
test("Yojana: retire late 50-65", "POST", "/yojana/retirement-plan",
     {"monthly_expenses": 80000, "current_age": 50, "retirement_age": 65, "current_corpus": 5000000})

# Dhan edge cases
print("\n--- Dhan (Health Score) ---")
test("Dhan: zero everything", "POST", "/dhan/health-score",
     {"income": 0, "expenses": 0, "monthly_savings": 0, "monthly_investments": 0})
test("Dhan: high earner", "POST", "/dhan/health-score",
     {"income": 500000, "expenses": 100000, "monthly_savings": 200000, "monthly_investments": 150000})

# Bazaar
print("\n--- Bazaar (Stocks) ---")
test("Bazaar: TCS stock", "POST", "/bazaar/stock-quote", {"symbol": "TCS"})
test("Bazaar: RELIANCE stock", "POST", "/bazaar/stock-quote", {"symbol": "RELIANCE"})
test("Bazaar: fake stock", "POST", "/bazaar/stock-quote", {"symbol": "NOTASTOCK123"})

# Niveshak
print("\n--- Niveshak (Portfolio) ---")
test("Niveshak: Basic SIP XIRR", "POST", "/niveshak/analyze", 
     {"holdings": [{"name": "HDFC Mid-Cap", "units": 100, "nav": 150, "allocation": 100}], 
      "sipAmount": 5000, "durationMonths": 24})
test("Niveshak: High Value XIRR", "POST", "/niveshak/analyze", 
     {"holdings": [{"name": "SBI Bluechip", "units": 500, "nav": 200, "allocation": 100}], 
      "sipAmount": 20000, "durationMonths": 60})

# Life Event edge
print("\n--- Life Event ---")
test("LifeEvent: education plan", "POST", "/life-event/plan",
     {"event_type": "education", "years_until": 10, "current_corpus": 500000})
test("LifeEvent: comprehensive married", "POST", "/life-event/comprehensive",
     {"event_type": "marriage", "years_until": 1, "current_corpus": 300000,
      "age": 28, "income": 80000})

# Couple edge
print("\n--- Couple Planner ---")
test("Couple: unequal income", "POST", "/couple/finances",
     {"person1_name": "X", "person1_income": 200000, "person2_name": "Y", "person2_income": 30000})
test("Couple: debt with savings", "POST", "/couple/debt-payoff",
     {"person1_name": "X", "person1_income": 100000, "person1_expenses": 50000, "person1_savings": 20000,
      "person2_name": "Y", "person2_income": 70000, "person2_expenses": 40000, "person2_savings": 15000,
      "debts": [{"name": "home loan", "balance": 3000000, "interest_rate": 8.5, "min_payment": 30000}],
      "strategy": "avalanche"})

# Print results
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
slow = sum(1 for r in results if r[0] == "SLOW")
total = len(results)

print("\n" + "=" * 60)
print("  FINAL: " + str(passed) + " PASS / " + str(failed) + " FAIL / " + str(slow) + " SLOW (" + str(total) + " total)")
print("=" * 60)

if failed > 0:
    print("\n  FAILURES:")
    for st, nm, dt in results:
        if st == "FAIL":
            print("    FAIL: " + nm)
            print("          " + dt)
