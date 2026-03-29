<p align="center">
  <h1 align="center">💰 AI Money Mentor</h1>
  <p align="center">
    <strong>India's First Multi-Agent Personal Finance Platform</strong><br/>
    9 specialized AI agents orchestrated by OpenClaw for tax planning, FIRE retirement, stock analysis, and couple's financial management.
  </p>
</p>

<p align="center">
  <a href="https://nextjs.org/"><img src="https://img.shields.io/badge/Next.js-16.2-000000?logo=nextdotjs" alt="Next.js"/></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.135-009688?logo=fastapi" alt="FastAPI"/></a>
  <a href="https://www.prisma.io/"><img src="https://img.shields.io/badge/Prisma-5.22-2D3748?logo=prisma" alt="Prisma"/></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12-3776AB?logo=python" alt="Python"/></a>
  <a href="#"><img src="https://img.shields.io/badge/OpenClaw-2026.3-blueviolet" alt="OpenClaw"/></a>
  <a href="#"><img src="https://img.shields.io/badge/Agents-9-orange" alt="Agents"/></a>
</p>

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Next.js Frontend                         │
│            Landing • 9 Agent Pages • Auth • Profile             │
│                          (Port 3000)                            │
└───────────────────────┬─────────────────────────────────────────┘
                        │  BFF Proxy (/api/*)
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)                   │
│                                                                 │
│     ┌─────────────────────────────────────────────────┐         │
│     │           DhanSarthi (Coordinator)              │         │
│     │     "The Brain" - routes every user query       │         │
│     │         to the right specialist agent           │         │
│     └──────┬──────┬──────┬──────┬──────┬──────┬───────┘         │
│            │      │      │      │      │      │                 │
│       ┌────▼─┐┌───▼──┐┌──▼───┐┌─▼────┐┌▼─────┐┌▼──────┐         │
│       │KarVid││Yojana││Bazaar││ Dhan ││Nivesh││ Vidhi │         │
│       │ Tax  ││ FIRE ││Stock ││Health││  MF  ││ Legal │         │
│       └──────┘└──────┘└──────┘└──────┘└──────┘└───────┘         │
│                                                                 │
│       ┌──────────────────┐      ┌──────────────────┐            │
│       │   Life Event     │      │  Couple Planner  │            │
│       │ Marriage, Baby   │      │  Joint Finance   │            │
│       └──────────────────┘      └──────────────────┘            │
│                                                                 │
└───────────────────────┬─────────────────────────────────────────┘
                        │
             ┌──────────▼──────────┐
             │  OpenClaw Gateway   │
             │   (Agent Swarm)     │
             │                     │
             │   Ollama / GLM-5    │
             │   (LLM Inference)   │
             └─────────────────────┘
```

> **How it works:** User sends a query → **DhanSarthi** analyzes intent → delegates to the right specialist agent (e.g., tax question → KarVid, retirement → Yojana) → returns the combined response. All delegation is handled via the **OpenClaw multi-agent swarm** protocol.

---

## 🤖 The 9 Agents

| # | Agent | Role | Key Features |
|---|-------|------|--------------|
| 1 | **KarVid** 🧾 | Tax Wizard | Old vs New regime comparison, 80C/80D deductions, capital gains, Indian Tax Laws DB |
| 2 | **YojanaKarta** 🎯 | FIRE Planner | FIRE number calculation, SIP recommendations, retirement planning |
| 3 | **BazaarGuru** 📈 | Market Analyst | NSE/BSE stock quotes, top gainers, NIFTY 50 data |
| 4 | **DhanRaksha** 💪 | Health Scorer | 8-factor financial health score with personalized suggestions |
| 5 | **Niveshak** 📊 | Portfolio Advisor | Dynamic XIRR iteration arrays, Sharpe Ratio, Risk matrices |
| 6 | **Vidhi** ⚖️ | Compliance Officer | SEBI regulations, legal disclaimers, financial law lookup |
| 7 | **DhanSarthi** 🧠 | Coordinator | Routes queries to the right agent via OpenClaw multi-agent swarm |
| 8 | **Life Event Advisor** 🎉 | Life Planner | Marriage, child birth, education — goal-based SIP planning |
| 9 | **Couple's Planner** 💑 | Joint Finance | Combined budgets, expense splitting, joint debt payoff strategies |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Next.js 16, React 19, TypeScript | App Router, SSR/SSG |
| **State** | Zustand + `useLocalStorage` | Persistent Form Caching |
| **Styling** | Tailwind CSS v4, shadcn/ui | Responsive UI components |
| **Backend** | FastAPI, Python 3.12 | REST API with 20+ endpoints |
| **Database** | Prisma 5, SQLite | User profiles, portfolios, chat history |
| **AI Orchestration** | OpenClaw 2026.3 | Multi-agent swarm coordination |
| **LLM Backend** | Ollama (local), GLM-5 Cloud | AI inference for agent responses |
| **Bots** | python-telegram-bot | Telegram integration |
| **Testing** | Jest, E2E Python tests | 26 deep + 25 routing = 51/51 tests passing |

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+ (3.12 recommended)

### 1. Clone

```bash
git clone https://github.com/Devguru-codes/AI-Money-Mentor.git
cd AI-Money-Mentor
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
.\venv\Scripts\activate

pip install -r requirements.txt
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npx prisma generate
npx prisma db push
npm run dev
```

### 4. Open in Browser

**Online Deployment:**
- **Frontend App:** [http://3.109.186.88:3000](http://3.109.186.88:3000)
- **API Docs:** [http://3.109.186.88:8000/docs](http://3.109.186.88:8000/docs)

**Local Deployment:**
- **Frontend App:** [http://localhost:3000](http://localhost:3000)
- **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔗 API Endpoints

### Frontend BFF Proxy Routes

| Route | Method | Backend Target |
|-------|--------|----------------|
| `/api/karvid` | POST | `/karvid/calculate-tax` |
| `/api/yojana` | POST | `/yojana/fire-number` |
| `/api/bazaar` | POST | `/bazaar/stock-quote` |
| `/api/dhan` | POST | `/dhan/health-score` |
| `/api/niveshak` | POST | `/niveshak/analyze` |
| `/api/vidhi` | GET | `/vidhi/disclaimers` |
| `/api/dhan-sarthi` | POST | `/dhan-sarthi/route` |
| `/api/life-event` | POST/GET | `/life-event/plan`, `/life-event/types` |
| `/api/couple-planner` | POST | `/couple/finances`, `/couple/budget`, `/couple/debt-payoff` |

### Backend Direct Endpoints (20+)

<details>
<summary>Click to expand full endpoint list</summary>

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info + all 9 agents |
| `/health` | GET | Health check |
| **KarVid** | | |
| `/karvid/calculate-tax` | POST | Calculate tax (old/new regime) |
| `/karvid/compare-regimes` | POST | Compare old vs new regime |
| `/karvid/80c` | POST | Calculate 80C deductions |
| `/karvid/capital-gains` | POST | STCG/LTCG tax |
| `/karvid/section/{section}` | GET | Tax law lookup |
| **YojanaKarta** | | |
| `/yojana/fire-number` | POST | Calculate FIRE number |
| `/yojana/sip-recommendation` | POST | SIP recommendation |
| `/yojana/retirement-plan` | POST | Full retirement plan |
| **BazaarGuru** | | |
| `/bazaar/stock-quote` | POST | Stock quote from NSE |
| `/bazaar/top-gainers` | GET | Top gaining stocks |
| `/bazaar/nifty50` | GET | NIFTY 50 list |
| **DhanRaksha** | | |
| `/dhan/health-score` | POST | 8-factor health score |
| **Niveshak** | | |
| `/niveshak/analyze` | POST | Portfolio analysis |
| `/niveshak/risk-metrics` | POST | Risk metrics |
| **Vidhi** | | |
| `/vidhi/disclaimers` | GET | SEBI disclaimers |
| `/vidhi/regulations` | GET | SEBI regulations |
| **Life Event** | | |
| `/life-event/types` | GET | Supported event types |
| `/life-event/plan` | POST | Event financial plan |
| `/life-event/comprehensive` | POST | Full event analysis |
| **Couple Planner** | | |
| `/couple/finances` | POST | Combined finances |
| `/couple/plan` | POST | Joint financial plan |
| `/couple/budget` | POST | 50/30/20 budget |
| `/couple/split-expense` | POST | Expense splitting |
| `/couple/debt-payoff` | POST | Joint debt strategy |

</details>

---

## ⚙️ Environment Variables

Create `.env` in the project root:

```env
# Database
DATABASE_URL="file:./frontend/prisma/dev.db"

# Backend URL (for frontend BFF proxy)
BACKEND_URL=http://localhost:8000

# OpenClaw Agent Swarm (configured via openclaw CLI on the server)
# Uses Ollama for local inference or GLM-5 Cloud for hosted AI
# No API key needed in .env — managed by OpenClaw gateway

# Telegram Bots (optional, get from @BotFather)
DHANSARTHI_BOT_TOKEN=your_token
KARVID_BOT_TOKEN=your_token
```

---

## 🧪 Testing

```bash
# Deep Agent Tests — 26/26
cd backend
python3 tests/deep_agent_test.py

# Greeting & Routing Tests — 25/25
python3 tests/greeting_test.py

# Build Verification
cd frontend
npx next build
```

---

## 📁 Project Structure

```
AI-Money-Mentor/
├── frontend/                    # Next.js 16 + React 19
│   ├── src/app/
│   │   ├── agents/              # 9 agent UI pages
│   │   │   ├── karvid/          # Tax Wizard
│   │   │   ├── yojana/          # FIRE Planner
│   │   │   ├── bazaar/          # Market Analyst
│   │   │   ├── dhan/            # Health Scorer
│   │   │   ├── niveshak/        # Portfolio Advisor
│   │   │   ├── vidhi/           # Compliance Officer
│   │   │   ├── dhan-sarthi/     # Coordinator (Swarm Hub)
│   │   │   ├── life-event/      # Life Event Planner
│   │   │   └── couple-planner/  # Joint Finance Manager
│   │   └── api/                 # 14 BFF proxy routes
│   ├── prisma/schema.prisma     # DB models
│   └── __tests__/               # Jest test suite
│
├── backend/                     # FastAPI + Python 3.12
│   ├── agents/
│   │   ├── karvid/              # Indian tax engine
│   │   ├── yojana/              # FIRE calculator
│   │   ├── bazaar/              # NSE stock data
│   │   ├── dhan/                # Health score (8-factor)
│   │   ├── niveshak/            # Portfolio analyzer
│   │   ├── vidhi/               # SEBI compliance
│   │   ├── dhan_sarthi/         # Query coordinator
│   │   ├── life_event/          # Life event planner
│   │   └── couple_planner/      # Couple finance planner
│   ├── bots/                    # Telegram bot integrations
│   ├── api_server.py            # FastAPI app (20+ endpoints)
│   ├── chat_bridge.py           # OpenClaw ↔ SQLite bridge
│   └── tests/e2e_test.py        # Integration tests
│
└── .openclaw/                   # Agent swarm configuration
    ├── agents/                  # 9 agent definitions
    └── SKILL.md                 # Swarm coordination rules
```

---

## 🚢 Deployment (EC2)

The project runs on an AWS EC2 instance:

```bash
# SSH into the instance
ssh -i your-key.pem ubuntu@your-ip

# Pull latest code
cd ~/ai-money-mentor
git pull origin main

# Start backend
cd backend
source venv/bin/activate
nohup uvicorn api_server:app --host 0.0.0.0 --port 8000 &

# Build & start frontend (production)
cd ../frontend
npm run build
npm run start -- -p 3000 &

# Or use PM2 (recommended — auto-restart on crash):
pm2 restart all
```

> **Note:** Ensure ports **3000** and **8000** are open in your AWS Security Group. The production instance uses PM2 for process management with 3 services: `frontend`, `backend`, and `openclaw-node`.

---

## 📄 License

MIT License — See [LICENSE](LICENSE)

---

## 👤 Author

**Devguru Tiwari**
- 🎓 IIIT Nagpur (BT23CSD060)
- 📧 bt23csd060@iiitn.ac.in
- 🐙 [@Devguru-codes](https://github.com/Devguru-codes)

---

<p align="center">
  <strong>🇮🇳 Built for India's Financial Future</strong><br/>
  <em>Empowering every Indian with AI-driven personal finance</em>
</p>
