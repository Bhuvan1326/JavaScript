.PHONY: help install dev build start stop test clean status

help:
	@echo "AI Money Mentor - Available Commands:"
	@echo "  make install  - Install all dependencies"
	@echo "  make dev      - Start development servers"
	@echo "  make build    - Build for production"
	@echo "  make start    - Start production servers"
	@echo "  make stop     - Stop all servers"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean build artifacts"
	@echo "  make status   - Check server status"

install:
	@echo "📦 Installing backend..."
	cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "📦 Installing frontend..."
	cd frontend && npm install && npx prisma generate
	@echo "✅ Done!"

dev:
	@./start-dev.sh

build:
	cd backend && source venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install && npx prisma generate && npm run build

start:
	@./start-prod.sh

stop:
	@pkill -f "uvicorn api_server:app" 2>/dev/null || true
	@pkill -f "next" 2>/dev/null || true
	@echo "Stopped."

test:
	cd backend && source venv/bin/activate && python -m pytest tests/ -v
	cd frontend && npm test

clean:
	rm -rf backend/__pycache__ frontend/.next
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

status:
	@curl -s http://localhost:8000/health && echo "" || echo "Backend not running"
