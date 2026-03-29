import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { userId, totalValue, xirr, sharpeRatio, sortinoRatio, holdings } = body

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const portfolio = await prisma.portfolio.upsert({
      where: { userId },
      update: {
        totalValue: totalValue || 0,
        xirr: xirr || 0,
        sharpeRatio: sharpeRatio || 0,
        sortinoRatio: sortinoRatio || 0,
        holdings: holdings || '[]',
      },
      create: {
        userId,
        totalValue: totalValue || 0,
        xirr: xirr || 0,
        sharpeRatio: sharpeRatio || 0,
        sortinoRatio: sortinoRatio || 0,
        holdings: holdings || '[]',
      },
    })

    return NextResponse.json({ portfolio }, { status: 201 })
  } catch (error: any) {
    console.error('Save portfolio error:', error)
    return NextResponse.json({ error: 'Failed to save: ' + error.message }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')
    if (!userId) return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    const portfolio = await prisma.portfolio.findUnique({
      where: { userId },
    })
    return NextResponse.json({ portfolio })
  } catch (error: any) {
    return NextResponse.json({ error: 'Failed to load: ' + error.message }, { status: 500 })
  }
}
