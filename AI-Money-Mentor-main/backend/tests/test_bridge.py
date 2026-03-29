#!/usr/bin/env python3
"""Test the bridge/chat endpoint with the real OpenClaw agent"""
import requests
import json
import sys

BASE = "http://localhost:8000"

print("=== Testing Bridge Chat Endpoint ===")
payload = {
    "message": "Hello, what can you help me with?",
    "user_id": "test-user",
    "agent_id": "dhan-sarthi"
}

print(f"POST {BASE}/bridge/chat")
print(f"Payload: {json.dumps(payload)}")
print("Waiting for OpenClaw response (may take 10-30s)...")

try:
    r = requests.post(f"{BASE}/bridge/chat", json=payload, timeout=120)
    print(f"\nStatus: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        print(f"Agent: {data.get('agent')}")
        print(f"Session: {data.get('session_id')}")
        print(f"History Count: {data.get('history_count')}")
        print(f"\n--- AI Response ---")
        print(data.get('response', 'NO RESPONSE'))
        print("--- End ---")
        
        # Test follow-up with session
        print("\n=== Testing Follow-up (Tax Query) ===")
        payload2 = {
            "message": "Calculate tax for 15 lakhs income",
            "user_id": "test-user",
            "agent_id": "dhan-sarthi",
            "session_id": data.get('session_id')
        }
        r2 = requests.post(f"{BASE}/bridge/chat", json=payload2, timeout=120)
        if r2.status_code == 200:
            data2 = r2.json()
            print(f"Agent: {data2.get('agent')}")
            print(f"\n--- AI Response ---")
            print(data2.get('response', 'NO RESPONSE'))
            print("--- End ---")
        else:
            print(f"Follow-up failed: {r2.status_code} {r2.text}")
    else:
        print(f"Error: {r.text}")
except Exception as e:
    print(f"Exception: {e}")
