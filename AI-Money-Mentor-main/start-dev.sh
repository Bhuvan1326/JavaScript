#!/bin/bash

# AI Money Mentor - Development Start Script
echo "🚀 Starting AI Money Mentor Development Environment..."

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check .env
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating template..."
    cat > .env << 'ENVEOF'
DATABASE_URL="file:./frontend/prisma/dev.db"
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_URL=http://localhost:8000
ENVEOF
fi

export $(cat .env | grep -v '^#' | xargs)

# Cleanup function
cleanup() {
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM

# Start Backend
echo "📦 Starting Backend (port 8000)..."
cd "$SCRIPT_DIR/backend"
[ ! -d "venv" ] && python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd "$SCRIPT_DIR"
sleep 3

# Start Frontend
echo "🎨 Starting Frontend (port 3000)..."
cd "$SCRIPT_DIR/frontend"
[ ! -d "node_modules" ] && npm install
npx prisma generate
npm run dev &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

echo "✅ Development environment started!"
echo "📱 Frontend: http://localhost:3000"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "Press Ctrl+C to stop."

wait $BACKEND_PID $FRONTEND_PID
