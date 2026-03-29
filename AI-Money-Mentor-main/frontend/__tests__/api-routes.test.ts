/**
 * API Routes Integration Tests
 * Tests all BFF proxy routes for the 9 AI Money Mentor agents
 */

// Mock fetch globally
const mockFetch = jest.fn()
global.fetch = mockFetch

// Mock NextRequest/NextResponse
jest.mock('next/server', () => ({
  NextRequest: jest.fn().mockImplementation((url: string, init?: any) => ({
    json: () => Promise.resolve(init?.body ? JSON.parse(init.body) : {}),
    url,
  })),
  NextResponse: {
    json: (data: any, init?: any) => ({
      status: init?.status || 200,
      json: () => Promise.resolve(data),
      data,
    }),
  },
}))

// ============ HELPER ============

function createMockRequest(body: any) {
  return { json: () => Promise.resolve(body) } as any
}

function mockBackendSuccess(data: any) {
  mockFetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve(data),
  })
}

function mockBackendDown() {
  mockFetch.mockRejectedValueOnce(new Error('ECONNREFUSED'))
}

// ============ KARVID (Tax) ============

describe('KarVid Tax API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies tax calculation to backend', async () => {
    const { POST } = await import('../src/app/api/karvid/route')
    mockBackendSuccess({ tax: 150000, regime: 'new' })

    const res = await POST(createMockRequest({ income: 1500000, regime: 'new' }))
    const data = await res.json()

    expect(mockFetch).toHaveBeenCalledTimes(1)
    expect(data.tax).toBe(150000)
  })

  it('returns 503 when backend is offline', async () => {
    const { POST } = await import('../src/app/api/karvid/route')
    mockBackendDown()

    const res = await POST(createMockRequest({ income: 1500000 }))
    const data = await res.json()

    expect(data.error).toBeDefined()
    expect(res.status).toBe(503)
  })
})

// ============ YOJANA (FIRE) ============

describe('Yojana FIRE API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies FIRE calculation to backend', async () => {
    const { POST } = await import('../src/app/api/yojana/route')
    mockBackendSuccess({ fire_number: 30000000, sip_needed: 25000 })

    const res = await POST(createMockRequest({ monthly_expenses: 50000 }))
    const data = await res.json()

    expect(data.fire_number).toBe(30000000)
  })
})

// ============ BAZAAR (Stocks) ============

describe('Bazaar Stock API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies stock quote to backend', async () => {
    const { POST } = await import('../src/app/api/bazaar/route')
    mockBackendSuccess({ symbol: 'RELIANCE', price: 2900 })

    const res = await POST(createMockRequest({ symbol: 'RELIANCE' }))
    const data = await res.json()

    expect(data.symbol).toBe('RELIANCE')
  })
})

// ============ NIVESHAK (Portfolio) ============

describe('Niveshak Portfolio API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies portfolio analysis to backend', async () => {
    const { POST } = await import('../src/app/api/niveshak/route')
    mockBackendSuccess({
      portfolio_value: 150000,
      estimated_xirr: 24.5,
      sharpe_ratio: 1.2
    })

    const res = await POST(createMockRequest({
      holdings: [{ name: 'HDFC', units: 100, nav: 1500, allocation: 100 }],
      sipAmount: 5000,
      durationMonths: 24
    }))
    const data = await res.json()

    expect(data.portfolio_value).toBe(150000)
    expect(data.estimated_xirr).toBe(24.5)
  })
})

// ============ DHAN (Health Score) ============

describe('Dhan Health Score API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies health score to backend', async () => {
    const { POST } = await import('../src/app/api/dhan/route')
    mockBackendSuccess({ score: 72, grade: 'B+' })

    const res = await POST(createMockRequest({ income: 100000, expenses: 60000 }))
    const data = await res.json()

    expect(data.score).toBe(72)
  })
})

// ============ VIDHI (Compliance) ============

describe('Vidhi Compliance API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies disclaimers GET to backend', async () => {
    const { GET } = await import('../src/app/api/vidhi/route')
    mockBackendSuccess({ disclaimers: ['Not financial advice'] })

    const res = await GET()
    const data = await res.json()

    expect(data.disclaimers).toContain('Not financial advice')
  })
})

// ============ LIFE-EVENT (New Agent) ============

describe('Life Event API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies life event plan to backend', async () => {
    const { POST } = await import('../src/app/api/life-event/route')
    mockBackendSuccess({
      event: 'marriage',
      future_cost: 2000000,
      sip_needed: 15000,
      is_achievable: true,
    })

    const res = await POST(createMockRequest({
      event_type: 'marriage',
      years_until: 5,
      current_corpus: 100000,
    }))
    const data = await res.json()

    expect(data.event).toBe('marriage')
    expect(data.sip_needed).toBe(15000)
    expect(data.is_achievable).toBe(true)
  })

  it('proxies event types GET to backend', async () => {
    const { GET } = await import('../src/app/api/life-event/route')
    mockBackendSuccess({
      marriage: { min: 500000, max: 5000000 },
      child_birth: { min: 100000, max: 500000 },
    })

    const res = await GET()
    const data = await res.json()

    expect(data.marriage).toBeDefined()
    expect(data.child_birth).toBeDefined()
  })

  it('returns 503 when backend is offline', async () => {
    const { POST } = await import('../src/app/api/life-event/route')
    mockBackendDown()

    const res = await POST(createMockRequest({ event_type: 'marriage', years_until: 5 }))
    const data = await res.json()

    expect(data.error).toBeDefined()
    expect(res.status).toBe(503)
  })
})

// ============ COUPLE-PLANNER (New Agent) ============

describe('Couple Planner API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies combined finances calculation', async () => {
    const { POST } = await import('../src/app/api/couple-planner/route')
    mockBackendSuccess({
      combined_income: 200000,
      combined_expenses: 120000,
      net_worth: 1500000,
    })

    const res = await POST(createMockRequest({
      action: 'finances',
      person1_name: 'Alice',
      person1_income: 120000,
      person2_name: 'Bob',
      person2_income: 80000,
    }))
    const data = await res.json()

    expect(data.combined_income).toBe(200000)
    expect(data.net_worth).toBe(1500000)
  })

  it('routes budget action correctly', async () => {
    const { POST } = await import('../src/app/api/couple-planner/route')
    mockBackendSuccess({ summary: { needs: 100000, wants: 60000, savings: 40000 } })

    const res = await POST(createMockRequest({
      action: 'budget',
      person1_name: 'Alice',
      person1_income: 120000,
      person2_name: 'Bob',
      person2_income: 80000,
    }))

    // Verify the fetch was called with /couple/budget endpoint
    const calledUrl = mockFetch.mock.calls[0][0]
    expect(calledUrl).toContain('/couple/budget')
  })

  it('routes debt-payoff action correctly', async () => {
    const { POST } = await import('../src/app/api/couple-planner/route')
    mockBackendSuccess({ strategy: 'avalanche', total_debt: 500000 })

    await POST(createMockRequest({
      action: 'debt-payoff',
      person1_name: 'A',
      person1_income: 100000,
      person2_name: 'B',
      person2_income: 100000,
    }))

    const calledUrl = mockFetch.mock.calls[0][0]
    expect(calledUrl).toContain('/couple/debt-payoff')
  })

  it('returns 503 when backend is offline', async () => {
    const { POST } = await import('../src/app/api/couple-planner/route')
    mockBackendDown()

    const res = await POST(createMockRequest({ action: 'finances' }))
    const data = await res.json()

    expect(data.error).toBeDefined()
    expect(res.status).toBe(503)
  })
})

// ============ DHAN-SARTHI (Coordinator) ============

describe('DhanSarthi Coordinator API', () => {
  beforeEach(() => mockFetch.mockClear())

  it('proxies routing query to backend', async () => {
    const { POST } = await import('../src/app/api/dhan-sarthi/route')
    mockBackendSuccess({ primary_agent: 'karvid', confidence: 0.95 })

    const res = await POST(createMockRequest({ query: 'calculate my tax' }))
    const data = await res.json()

    expect(data.primary_agent).toBe('karvid')
  })
})

// ============ REGRESSION GUARDS ============

describe('Regression Guards', () => {
  const fs = require('fs')
  const path = require('path')

  it('no agent page calls localhost:8000 directly', () => {
    const agentsDir = path.join(__dirname, '..', 'src', 'app', 'agents')
    if (!fs.existsSync(agentsDir)) return

    const agentFolders = fs.readdirSync(agentsDir)
    for (const folder of agentFolders) {
      const pagePath = path.join(agentsDir, folder, 'page.tsx')
      if (fs.existsSync(pagePath)) {
        const content = fs.readFileSync(pagePath, 'utf8')
        expect(content).not.toContain('localhost:8000')
        expect(content).not.toContain('127.0.0.1:8000')
      }
    }
  })

  it('all proxy routes use BACKEND_URL env var', () => {
    const apiDir = path.join(__dirname, '..', 'src', 'app', 'api')
    if (!fs.existsSync(apiDir)) return

    // Auth and save routes use Prisma directly, not the backend proxy
    const skipDirs = ['auth', 'save']

    const checkDir = (dir: string) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true })
      for (const entry of entries) {
        if (skipDirs.includes(entry.name)) continue
        const fullPath = path.join(dir, entry.name)
        if (entry.isDirectory()) {
          checkDir(fullPath)
        } else if (entry.name === 'route.ts') {
          const content = fs.readFileSync(fullPath, 'utf8')
          expect(content).toContain('BACKEND_URL')
        }
      }
    }
    checkDir(apiDir)
  })
})
