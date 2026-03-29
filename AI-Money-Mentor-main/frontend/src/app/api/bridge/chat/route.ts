import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://127.0.0.1:8000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { message, user_id, agent_id, session_id } = body

    if (!message || !user_id) {
      return NextResponse.json(
        { error: 'message and user_id are required' },
        { status: 400 }
      )
    }

    const response = await fetch(`${BACKEND_URL}/bridge/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        user_id,
        agent_id: agent_id || 'dhan-sarthi',
        session_id: session_id || null,
      }),
    })

    if (!response.ok) {
      const errorText = await response.text()
      return NextResponse.json(
        { error: `Bridge error: ${response.status}`, details: errorText },
        { status: response.status }
      )
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error: any) {
    return NextResponse.json(
      { error: 'Bridge backend is offline. Ensure FastAPI is running on port 8000.' },
      { status: 503 }
    )
  }
}
