import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { userId, agentType, query, response } = body

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const chatMessage = await prisma.chatMessage.create({
      data: {
        userId,
        agentType: agentType || 'dhan-sarthi',
        query: query || '',
        response: response || '',
      },
    })

    return NextResponse.json({ chatMessage }, { status: 201 })
  } catch (error: any) {
    console.error('Save chat error:', error)
    return NextResponse.json({ error: 'Failed to save: ' + error.message }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')
    const limit = parseInt(searchParams.get('limit') || '20', 10)

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const messages = await prisma.chatMessage.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' },
      take: limit,
    })

    // Return in chronological order
    return NextResponse.json({ messages: messages.reverse() })
  } catch (error: any) {
    console.error('Load chat error:', error)
    return NextResponse.json({ error: 'Failed to load: ' + error.message }, { status: 500 })
  }
}
