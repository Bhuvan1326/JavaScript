#!/bin/bash
cd /home/ubuntu/ai-money-mentor
source venv/bin/activate

# Check if already running
if pgrep -f "uvicorn.*api_server" > /dev/null; then
    echo "API server already running"
    exit 0
fi

# Start API server
nohup python -c "
import uvicorn
from api_server import app
uvicorn.run(app, host='0.0.0.0', port=8000)
" > /tmp/api_server.log 2>&1 &

echo "API server started on port 8000"
