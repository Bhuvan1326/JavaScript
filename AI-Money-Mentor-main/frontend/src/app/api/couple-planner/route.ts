import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const action = body.action || 'finances'

    // Map actions to backend endpoints
    const endpointMap: Record<string, string> = {
      'finances': '/couple/finances',
      'split-expense': '/couple/split-expense',
      'plan': '/couple/plan',
      'budget': '/couple/budget',
      'goals': '/couple/goals',
      'debt-payoff': '/couple/debt-payoff',
    }

    const endpoint = endpointMap[action] || '/couple/finances'

    const response = await fetch(`${BACKEND_URL}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      return NextResponse.json(
        { error: errorData.detail || 'Backend returned an error', status: response.status },
        { status: response.status }
      )
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error: any) {
    console.error('Couple Planner API Error:', error)
    return NextResponse.json(
      { error: 'Backend is offline. Please ensure the FastAPI server is running on port 8000.' },
      { status: 503 }
    )
  }
}