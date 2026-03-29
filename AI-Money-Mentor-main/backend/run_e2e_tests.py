import sys
import subprocess
import time
import os

# Set PYTHONPATH to include backend
env = os.environ.copy()
env["PYTHONPATH"] = os.path.abspath(os.path.dirname(__file__))

print("Starting server...")
# Start server
server = subprocess.Popen([sys.executable, "-m", "uvicorn", "api_server:app", "--port", "8000"], env=env)

print("Waiting for server to start...")
time.sleep(5)

print("\n--- Running deep_agent_test.py ---")
subprocess.run([sys.executable, "tests/deep_agent_test.py"], env=env)

print("\n--- Running greeting_test.py ---")
subprocess.run([sys.executable, "tests/greeting_test.py"], env=env)

print("\nKilling server...")
server.terminate()
server.wait()
