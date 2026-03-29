import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { userId, name, phone } = body

    if (!userId) {
      return NextResponse.json({ error: 'userId is required' }, { status: 400 })
    }

    const user = await prisma.user.update({
      where: { id: userId },
      data: {
        ...(name !== undefined && { name }),
        ...(phone !== undefined && { phone }),
      },
    })

    return NextResponse.json({ user })
  } catch (error: any) {
    console.error('Profile update error:', error)
    if (error.code === 'P2025') {
      return NextResponse.json({ error: 'User not found' }, { status: 404 })
    }
    return NextResponse.json(
      { error: 'Update failed: ' + error.message },
      { status: 500 }
    )
  }
}
