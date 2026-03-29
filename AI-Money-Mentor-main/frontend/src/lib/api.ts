import axios from 'axios'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'
const FRONTEND_URL = process.env.NEXT_PUBLIC_FRONTEND_URL || 'http://localhost:3000'

export const backendApi = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const frontendApi = axios.create({
  baseURL: FRONTEND_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Tax Calculator API
export const karvidApi = {
  calculateTax: async (data: any) => {
    const response = await backendApi.post('/karvid/calculate-tax', data)
    return response.data
  },
  compareRegimes: async (data: any) => {
    const response = await backendApi.post('/karvid/compare-regimes', data)
    return response.data
  },
  getSection: async (sectionId: string) => {
    const response = await backendApi.get(`/karvid/section/${sectionId}`)
    return response.data
  },
}

// FIRE Planner API
export const yojanaApi = {
  calculateFIRE: async (data: any) => {
    const response = await backendApi.post('/yojana/fire-number', data)
    return response.data
  },
}

// Stock Quotes API
export const bazaarApi = {
  getStockQuote: async (data: any) => {
    const response = await backendApi.post('/bazaar/stock-quote', data)
    return response.data
  },
}

// Health Score API
export const dhanApi = {
  calculateHealthScore: async (data: any) => {
    const response = await backendApi.post('/dhan/health-score', data)
    return response.data
  },
}

// MF Portfolio API
export const niveshakApi = {
  calculateXIRR: async (data: any) => {
    const response = await backendApi.post('/niveshak/xirr', data)
    return response.data
  },
  analyzePortfolio: async (data: any) => {
    const response = await backendApi.post('/niveshak/analyze', data)
    return response.data
  },
}

// Life Event API
export const lifeEventApi = {
  planEvent: async (data: any) => {
    const response = await backendApi.post('/life-event/plan', data)
    return response.data
  },
  getEventTypes: async () => {
    const response = await backendApi.get('/life-event/types')
    return response.data
  },
}

// Couple Planner API
export const couplePlannerApi = {
  planFinances: async (data: any) => {
    const response = await backendApi.post('/couple/finances', data)
    return response.data
  },
  splitExpense: async (data: any) => {
    const response = await backendApi.post('/couple/split-expense', data)
    return response.data
  },
}

// Compliance API
export const vidhiApi = {
  getDisclaimers: async () => {
    const response = await backendApi.get('/vidhi/disclaimers')
    return response.data
  },
}

// Query Routing API
export const dhanSarthiApi = {
  route: async (query: string) => {
    const response = await backendApi.post('/dhan-sarthi/route', { query })
    return response.data
  },
}

// Format currency in INR
export const formatINR = (amount: number) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(amount)
}

// Format percentage
export const formatPercent = (value: number) => {
  return `${value.toFixed(2)}%`
}
