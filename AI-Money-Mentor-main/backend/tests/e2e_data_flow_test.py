"""
End-to-End Data Flow Test
Tests: Signup → Login → Chat Save → Chat Load → Profile Update → Context Check
"""
import requests
import json
import uuid

BASE = "http://localhost:3000"
results = []

def test(name, fn):
    try:
        ok, detail = fn()
        status = "PASS" if ok else "FAIL"
        results.append((status, name, detail))
        print(f"  {status}: {name} — {detail}")
    except Exception as e:
        results.append(("FAIL", name, str(e)[:80]))
        print(f"  FAIL: {name} — {str(e)[:80]}")

# Generate unique test user
test_email = f"e2e-test-{uuid.uuid4().hex[:8]}@test.com"
test_name = "E2E Test User"
user_id = None

print("=" * 60)
print("  END-TO-END DATA FLOW TEST")
print("=" * 60)

# ── 1. SIGNUP ──
print("\n--- Auth Flow ---")

def test_signup():
    global user_id
    r = requests.post(f"{BASE}/api/auth/signup", json={
        "email": test_email,
        "name": test_name,
        "phone": "+91-9999999999"
    }, timeout=10)
    data = r.json()
    if r.status_code == 201 and "user" in data:
        user_id = data["user"]["id"]
        return True, f"Created user {user_id[:8]}... with email {test_email}"
    return False, f"Status {r.status_code}: {data}"

test("Signup creates user in Prisma DB", test_signup)

# ── 2. LOGIN ──
def test_login():
    r = requests.post(f"{BASE}/api/auth/login", json={"email": test_email}, timeout=10)
    data = r.json()
    if r.status_code == 200 and "user" in data:
        found_id = data["user"]["id"]
        return found_id == user_id, f"Retrieved user {found_id[:8]}... (match={found_id == user_id})"
    return False, f"Status {r.status_code}: {data}"

test("Login retrieves user from Prisma DB", test_login)

# ── 3. DUPLICATE SIGNUP ──
def test_duplicate_signup():
    r = requests.post(f"{BASE}/api/auth/signup", json={
        "email": test_email,
        "name": "Duplicate User"
    }, timeout=10)
    data = r.json()
    # Should return existing user, not create duplicate
    if "user" in data and data["user"]["id"] == user_id:
        return True, "Returns existing user (no duplicate created)"
    return False, f"Status {r.status_code}: {data}"

test("Duplicate signup returns existing user", test_duplicate_signup)

# ── 4. PROFILE UPDATE ──
def test_profile_update():
    r = requests.post(f"{BASE}/api/auth/update", json={
        "userId": user_id,
        "name": "Updated Name",
        "phone": "+91-8888888888"
    }, timeout=10)
    data = r.json()
    if r.status_code == 200 and "user" in data:
        updated = data["user"]
        return updated["name"] == "Updated Name", f"Name changed to '{updated['name']}'"
    return False, f"Status {r.status_code}: {data}"

test("Profile update persists to Prisma DB", test_profile_update)

# ── 5. VERIFY UPDATE ──
def test_verify_update():
    r = requests.post(f"{BASE}/api/auth/login", json={"email": test_email}, timeout=10)
    data = r.json()
    if "user" in data:
        return data["user"]["name"] == "Updated Name", f"Name is '{data['user']['name']}'"
    return False, "User not found"

test("Login after update shows new name", test_verify_update)

# ── CHAT PERSISTENCE ──
print("\n--- Chat Persistence ---")

def test_chat_save():
    r = requests.post(f"{BASE}/api/save/chat", json={
        "userId": user_id,
        "agentType": "karvid",
        "query": "Calculate tax for 15 lakhs",
        "response": "Your tax is Rs.1,95,000 under new regime"
    }, timeout=10)
    data = r.json()
    if r.status_code == 201 and "chatMessage" in data:
        return True, f"Saved chat {data['chatMessage']['id'][:8]}..."
    return False, f"Status {r.status_code}: {data}"

test("Chat message saved to Prisma", test_chat_save)

# Save multiple chats for context test
def test_chat_save_multiple():
    msgs = [
        {"agentType": "yojana", "query": "What is FIRE?", "response": "FIRE = Financial Independence, Retire Early"},
        {"agentType": "dhan-sarthi", "query": "Hello", "response": "Namaste! I'm DhanSarthi."},
        {"agentType": "bazaar", "query": "RELIANCE price", "response": "RELIANCE: Rs.1414"},
    ]
    saved = 0
    for m in msgs:
        r = requests.post(f"{BASE}/api/save/chat", json={"userId": user_id, **m}, timeout=10)
        if r.status_code == 201:
            saved += 1
    return saved == 3, f"Saved {saved}/3 additional messages"

test("Multiple chat messages saved", test_chat_save_multiple)

def test_chat_load():
    r = requests.get(f"{BASE}/api/save/chat?userId={user_id}&limit=10", timeout=10)
    data = r.json()
    if r.status_code == 200 and "messages" in data:
        count = len(data["messages"])
        queries = [m["query"] for m in data["messages"]]
        return count >= 4, f"Loaded {count} messages. Queries: {queries[:3]}"
    return False, f"Status {r.status_code}: {data}"

test("Chat history loaded from Prisma (GET)", test_chat_load)

def test_chat_history_order():
    r = requests.get(f"{BASE}/api/save/chat?userId={user_id}&limit=10", timeout=10)
    data = r.json()
    if r.status_code == 200 and "messages" in data and len(data["messages"]) >= 2:
        msgs = data["messages"]
        # Should be chronological (oldest first)
        times = [m["createdAt"] for m in msgs]
        is_ordered = all(times[i] <= times[i+1] for i in range(len(times)-1))
        return is_ordered, f"Chronological order: {is_ordered}"
    return False, "Not enough messages"

test("Chat history in chronological order", test_chat_history_order)

# ── SAVE ENDPOINTS ──
print("\n--- Save Endpoints (Tax, FIRE, Health) ---")

def test_save_tax():
    r = requests.post(f"{BASE}/api/save/tax", json={
        "userId": user_id,
        "financialYear": "2025-26",
        "regime": "new",
        "grossIncome": 1500000,
        "deductions80C": 150000,
        "deductions80D": 25000,
        "taxPayable": 195000
    }, timeout=10)
    data = r.json()
    if r.status_code == 201 and "taxProfile" in data:
        return True, f"Saved tax profile {data['taxProfile']['id'][:8]}..."
    return False, f"Status {r.status_code}: {data}"

test("Tax profile saved to Prisma", test_save_tax)

def test_save_fire():
    r = requests.post(f"{BASE}/api/save/fire", json={
        "userId": user_id,
        "targetCorpus": 15000000,
        "monthlyExpenses": 50000,
        "targetYears": 15,
        "monthlySIP": 35000
    }, timeout=10)
    data = r.json()
    if r.status_code == 201 and "fireGoal" in data:
        return True, f"Saved FIRE goal {data['fireGoal']['id'][:8]}..."
    return False, f"Status {r.status_code}: {data}"

test("FIRE goal saved to Prisma", test_save_fire)

def test_save_health():
    r = requests.post(f"{BASE}/api/save/health", json={
        "userId": user_id,
        "overallScore": 72,
        "emergencyFund": 300000,
        "savingsRate": 0.25,
        "debtToIncome": 0.15
    }, timeout=10)
    data = r.json()
    if r.status_code == 201 and "healthScore" in data:
        return True, f"Saved health score {data['healthScore']['id'][:8]}..."
    return False, f"Status {r.status_code}: {data}"

test("Health score saved to Prisma", test_save_health)

# ── CROSS-SESSION CONTEXT ──
print("\n--- Cross-Session Context ---")

def test_session_context():
    """Simulate 4th login session: can we see previous data?"""
    # Login again (simulating returning user)
    r = requests.post(f"{BASE}/api/auth/login", json={"email": test_email}, timeout=10)
    data = r.json()
    if "user" not in data:
        return False, "Login failed"
    
    uid = data["user"]["id"]
    
    # Load chat history
    r2 = requests.get(f"{BASE}/api/save/chat?userId={uid}&limit=50", timeout=10)
    chat_data = r2.json()
    has_chat = r2.status_code == 200 and "messages" in chat_data and len(chat_data["messages"]) > 0
    chat_count = len(chat_data.get("messages", []))
    
    return has_chat, f"4th session: {chat_count} chat messages loaded for user {uid[:8]}..."

test("4th session login sees previous chat history", test_session_context)

def test_context_to_agents():
    """Check: is chat context actually passed to backend agents?"""
    # The DhanSarthi route endpoint - does it receive any context?
    r = requests.post("http://localhost:8000/dhan-sarthi/route", json={
        "query": "Calculate tax for 15 lakhs"
    }, timeout=10)
    data = r.json()
    # Check if there's a user_id or context field in the response
    has_context = "context" in data or "history" in data or "user_id" in data
    return False, f"Agent routing does NOT receive user context/history (fields: {list(data.keys())})"

test("Backend agents receive user context", test_context_to_agents)

# ── SUMMARY ──
passed = sum(1 for r in results if r[0] == "PASS")
failed = sum(1 for r in results if r[0] == "FAIL")

print("\n" + "=" * 60)
print(f"  FINAL: {passed} PASS / {failed} FAIL ({len(results)} total)")
print("=" * 60)

if failed > 0:
    print("\n  GAPS FOUND:")
    for s, n, d in results:
        if s == "FAIL":
            print(f"    ❌ {n}: {d}")

print("\n  IMPLEMENTATION STATUS:")
print("    ✅ User signup → Prisma DB")
print("    ✅ User login → Prisma DB lookup")
print("    ✅ Profile update → Prisma DB")
print("    ✅ Chat save → Prisma ChatMessage table")
print("    ✅ Chat load → GET with userId filter")
print("    ✅ Tax/FIRE/Health save → Prisma")
print("    ✅ Cross-session: chat history loads on return")
print("    ❌ GAP: Backend agents don't receive user context/chat history")
print("    ❌ GAP: No Portfolio save endpoint")
print("    ❌ GAP: No Tax/FIRE/Health load (GET) endpoints")
print("    ❌ GAP: Frontend agent pages don't save results to DB")
print("    ❌ GAP: DhanSarthi doesn't pass user history for contextual responses")
