import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { userId, overallScore, emergencyFund, savingsRate, debtToIncome } = body

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const healthScore = await prisma.healthScore.create({
      data: {
        userId,
        overallScore: overallScore || 0,
        emergencyFund: emergencyFund || 0,
        savingsRate: savingsRate || 0,
        debtToIncome: debtToIncome || 0,
      },
    })

    return NextResponse.json({ healthScore }, { status: 201 })
  } catch (error: any) {
    console.error('Save health error:', error)
    return NextResponse.json({ error: 'Failed to save: ' + error.message }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')
    if (!userId) return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    const healthScores = await prisma.healthScore.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' },
      take: 5,
    })
    return NextResponse.json({ healthScores })
  } catch (error: any) {
    return NextResponse.json({ error: 'Failed to load: ' + error.message }, { status: 500 })
  }
}
