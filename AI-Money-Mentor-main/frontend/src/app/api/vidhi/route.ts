import { NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000'

export async function GET() {
  try {
    const response = await fetch(`${BACKEND_URL}/vidhi/disclaimers`, {
      method: 'GET',
    })

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Backend returned an error', status: response.status },
        { status: response.status }
      )
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error: any) {
    return NextResponse.json(
      { error: 'Backend is offline. Please ensure the FastAPI server is running on port 8000.' },
      { status: 503 }
    )
  }
}
