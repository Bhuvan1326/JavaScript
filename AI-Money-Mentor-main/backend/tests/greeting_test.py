import requests
import json

BASE = "http://localhost:8000"
results = []

def test(name, body, expected_agent, expected_intent=None):
    try:
        r = requests.post(BASE + "/dhan-sarthi/route", json=body, timeout=8)
        if r.status_code == 200:
            data = r.json()
            agent = data.get("primary_agent", "unknown")
            intent = data.get("intent", "")
            response = data.get("response", "")
            
            agent_ok = agent == expected_agent
            intent_ok = expected_intent is None or intent == expected_intent
            
            if agent_ok and intent_ok:
                results.append(("PASS", name, agent + " / " + intent))
                if response:
                    print("  PASS: " + name + " -> " + agent + " / " + intent)
                    print("        Response: " + response[:100])
                else:
                    print("  PASS: " + name + " -> " + agent + " / " + intent)
            else:
                results.append(("FAIL", name, "got " + agent + "/" + intent + ", want " + expected_agent))
                print("  FAIL: " + name + " -> " + agent + "/" + intent + " (want " + expected_agent + ")")
        else:
            results.append(("FAIL", name, str(r.status_code)))
            print("  FAIL: " + name + " -> " + str(r.status_code))
    except Exception as e:
        results.append(("FAIL", name, str(e)[:60]))
        print("  FAIL: " + name + " -> " + str(e)[:60])

print("=" * 60)
print("  DHANSARTHI GREETING & GENERIC QUERY TEST")
print("=" * 60)

# Greetings
print("\n--- Greetings ---")
test("Hello", {"query": "hello"}, "dhan-sarthi", "greeting")
test("Hi there", {"query": "hi there"}, "dhan-sarthi", "greeting")
test("Hey!", {"query": "hey!"}, "dhan-sarthi", "greeting")
test("Namaste", {"query": "namaste"}, "dhan-sarthi", "greeting")
test("Good morning", {"query": "good morning"}, "dhan-sarthi", "greeting")
test("Good evening", {"query": "good evening"}, "dhan-sarthi", "greeting")

# Help / What can you do
print("\n--- Help / About ---")
test("What can you do?", {"query": "what can you do?"}, "dhan-sarthi", "help")
test("Who are you?", {"query": "who are you?"}, "dhan-sarthi", "help")
test("Help me", {"query": "help me"}, "dhan-sarthi", "help")
test("What is this?", {"query": "what is this?"}, "dhan-sarthi")

# Thanks
print("\n--- Thanks / Goodbye ---")
test("Thank you!", {"query": "thank you!"}, "dhan-sarthi", "thanks")
test("Thanks a lot", {"query": "thanks a lot"}, "dhan-sarthi", "thanks")
test("Dhanyavaad", {"query": "dhanyavaad"}, "dhan-sarthi", "thanks")
test("Bye!", {"query": "bye!"}, "dhan-sarthi", "thanks")

# Generic explain
print("\n--- Generic Explain ---")
test("Explain how it works", {"query": "explain how it works"}, "dhan-sarthi", "explain")
test("What is AI money mentor", {"query": "what is ai money mentor"}, "dhan-sarthi")

# Finance-specific queries should NOT route to DhanSarthi
print("\n--- Finance queries (should NOT route to DhanSarthi) ---")
test("Hello, calculate my tax", {"query": "hello, calculate my tax for 15 lakh"}, "karvid")
test("Hi, what is RELIANCE stock", {"query": "hi, what is reliance stock price"}, "bazaar")
test("Help me retire early", {"query": "help me with fire retirement planning"}, "yojana")
test("Thanks, but explain my health score", {"query": "explain my financial health score"}, "dhan")

# All original routing should still work
print("\n--- Original routing (regression test) ---")
test("Tax calculation", {"query": "calculate income tax"}, "karvid")
test("Stock price", {"query": "TCS share price today"}, "bazaar")
test("FIRE planning", {"query": "when can I retire early"}, "yojana")
test("Marriage plan", {"query": "getting married next year"}, "life-event")
test("Couple budget", {"query": "joint budget with my wife"}, "couple-planner")

# Summary
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")
print("\n" + "=" * 60)
print("  FINAL: " + str(passed) + " PASS / " + str(failed) + " FAIL (" + str(len(results)) + " total)")
print("=" * 60)
if failed > 0:
    print("\n  FAILURES:")
    for s, n, d in results:
        if s == "FAIL":
            print("    " + n + ": " + d)
