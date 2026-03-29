import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { userId, financialYear, regime, grossIncome, deductions80C, deductions80D, taxPayable } = body

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const taxProfile = await prisma.taxProfile.create({
      data: {
        userId,
        financialYear: financialYear || '2025-26',
        regime: regime || 'new',
        grossIncome: grossIncome || 0,
        deductions80C: deductions80C || 0,
        deductions80D: deductions80D || 0,
        taxPayable: taxPayable || 0,
      },
    })

    return NextResponse.json({ taxProfile }, { status: 201 })
  } catch (error: any) {
    console.error('Save tax error:', error)
    return NextResponse.json({ error: 'Failed to save: ' + error.message }, { status: 500 })
  }
}

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url)
    const userId = searchParams.get('userId')
    if (!userId) return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    const taxProfiles = await prisma.taxProfile.findMany({
      where: { userId },
      orderBy: { createdAt: 'desc' },
      take: 5,
    })
    return NextResponse.json({ taxProfiles })
  } catch (error: any) {
    return NextResponse.json({ error: 'Failed to load: ' + error.message }, { status: 500 })
  }
}
