# CLAUDE.md — AI Money Mentor Architecture Quick Reference

## Deployed URLs
- **Frontend:** http://3.109.186.88:3000
- **Backend API:** http://3.109.186.88:8000
- **API Docs:** http://3.109.186.88:8000/docs
- **GitHub:** https://github.com/Devguru-codes/AI-Money-Mentor

## Backend Endpoints (FastAPI on Port 8000)

### Core
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info + agent list |
| `/health` | GET | Health check |
| `/ai/chat` | POST | AI chat endpoint |

### Niveshak (MF Portfolio)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/niveshak/xirr` | POST | Calculate XIRR for portfolio |
| `/niveshak/risk-metrics` | POST | Get portfolio risk metrics |
| `/niveshak/analyze` | POST | Full portfolio analysis with XIRR + Sharpe |

### KarVid (Tax Wizard)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/karvid/calculate-tax` | POST | Income tax (old/new regime) |
| `/karvid/compare-regimes` | POST | Side-by-side regime comparison |
| `/karvid/80c` | POST | Section 80C deductions |
| `/karvid/capital-gains` | POST | STCG/LTCG tax |
| `/karvid/section/{section}` | GET | Tax law lookup |
| `/karvid/capital-gains-info/{asset_type}` | GET | Capital gains info |
| `/karvid/tax-slabs/{regime}` | GET | Tax slabs for regime |

### YojanaKarta (FIRE Planner)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/yojana/fire-number` | POST | FIRE number calculation |
| `/yojana/sip-recommendation` | POST | SIP plan |
| `/yojana/retirement-plan` | POST | Full retirement plan |

### BazaarGuru (Market Research)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/bazaar/stock-quote` | POST | NSE stock quote |
| `/bazaar/top-gainers` | GET | Top gaining stocks |
| `/bazaar/nifty50` | GET | NIFTY 50 list |

### DhanRaksha (Financial Health)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dhan/health-score` | POST | 8-factor health score |

### Vidhi (Compliance)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/vidhi/disclaimers` | GET | SEBI compliance disclaimers |
| `/vidhi/regulations` | GET | SEBI regulations |
| `/vidhi/constitution/{article}` | GET | Constitution provision |
| `/vidhi/income-tax-section/{section}` | GET | Income Tax Act section |
| `/vidhi/sebi-regulation/{name}` | GET | SEBI regulation detail |
| `/vidhi/rbi-regulation/{name}` | GET | RBI regulation detail |

### DhanSarthi (Coordinator)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/dhan-sarthi/route` | POST | Query routing (greeting-aware) |
| `/latency-stats` | GET | Latency statistics |

### Life Event Advisor
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/life-event/types` | GET | Supported event types |
| `/life-event/plan` | POST | Event financial plan |
| `/life-event/comprehensive` | POST | Full event analysis |

### Couple Planner
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/couple/finances` | POST | Combined finances |
| `/couple/plan` | POST | Joint financial plan |
| `/couple/budget` | POST | 50/30/20 budget |
| `/couple/split-expense` | POST | Expense splitting |
| `/couple/goals` | POST | SIP for shared goals |
| `/couple/debt-payoff` | POST | Joint debt strategy |

### Chat Bridge (OpenClaw)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/bridge/chat` | POST | Bridge frontend to OpenClaw agents |
| `/bridge/history/{user_id}/{session_id}` | GET | Get chat history |
| `/bridge/history/{user_id}/{session_id}` | DELETE | Clear chat history |
| `/bridge/sessions/{user_id}` | GET | List chat sessions |

## Frontend BFF Proxy Routes (Next.js on Port 3000)

| BFF Route | Backend Target |
|-----------|----------------|
| `/api/auth/login` | Prisma user lookup (local) |
| `/api/auth/signup` | Prisma user create (local) |
| `/api/auth/update` | Prisma user update (local) |
| `/api/save/chat` | POST/GET chat history (Prisma) |
| `/api/save/fire` | POST save FIRE goals |
| `/api/save/health` | POST save health scores |
| `/api/save/tax` | POST save tax profiles |
| `/api/dhan-sarthi` | → `/dhan-sarthi/route` |
| `/api/karvid` | → `/karvid/calculate-tax` |
| `/api/yojana` | → `/yojana/fire-number` |
| `/api/bazaar` | → `/bazaar/stock-quote` |
| `/api/dhan` | → `/dhan/health-score` |
| `/api/niveshak` | → `/niveshak/analyze` |
| `/api/vidhi` | → `/vidhi/disclaimers` |
| `/api/life-event` | → `/life-event/plan` (POST) and `/life-event/types` (GET) |
| `/api/couple-planner` | → `/couple/*` endpoints |
| `/api/bridge/chat` | → `/bridge/chat` |

## Frontend Pages

| Page | Path | Component |
|------|------|-----------|
| Home/Landing | `/` | `app/page.tsx` |
| Agents Hub | `/agents` | `app/agents/page.tsx` |
| DhanSarthi Chat | `/agents/dhan-sarthi` | Full chat UI with streaming |
| KarVid Tax | `/agents/karvid` | Form + comparison + AI chat |
| YojanaKarta FIRE | `/agents/yojana` | FIRE calculator + AI chat |
| BazaarGuru | `/agents/bazaar` | Stock search + AI chat |
| DhanRaksha | `/agents/dhan` | Health score form + AI chat |
| Vidhi | `/agents/vidhi` | Legal/compliance + AI chat |
| Life Event | `/agents/life-event` | Event planner + AI chat |
| Couple Planner | `/agents/couple-planner` | Joint finance + AI chat |
| Login | `/login` | Email/Telegram auth |
| Profile | `/profile` | User profile update |

## Tech Stack
- **Frontend:** Next.js 16, React 19, TypeScript, Tailwind CSS v4, shadcn/ui
- **Backend:** FastAPI, Python 3.11+
- **Database:** Prisma 5 + SQLite (frontend), SQLite (backend chat bridge)
- **State:** Zustand + localStorage
- **AI:** OpenClaw agent swarm, Ollama/GLM-5
- **EC2:** ubuntu@3.109.186.88

## Environment Variables
- `BACKEND_URL` — FastAPI server URL (used by Next.js API routes, server-side)
- `NEXT_PUBLIC_BACKEND_URL` — Backend URL (used by client-side api.ts)
- `NEXT_PUBLIC_FRONTEND_URL` — Frontend URL (used by client-side api.ts)
- `DATABASE_URL` — Prisma SQLite path
