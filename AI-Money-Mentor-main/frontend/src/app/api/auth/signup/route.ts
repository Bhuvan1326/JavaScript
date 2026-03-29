import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import crypto from 'crypto'

function hashPassword(password: string): string {
  const salt = crypto.randomBytes(16).toString('hex')
  const hash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex')
  return `${salt}:${hash}`
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { telegramId, email, name, phone, password } = body

    if (!telegramId && !email) {
      return NextResponse.json(
        { error: 'Please provide either telegramId or email' },
        { status: 400 }
      )
    }

    // Password required for email signup
    if (email && !password) {
      return NextResponse.json(
        { error: 'Password is required' },
        { status: 400 }
      )
    }

    if (password && password.length < 6) {
      return NextResponse.json(
        { error: 'Password must be at least 6 characters' },
        { status: 400 }
      )
    }

    // Check if user already exists
    if (telegramId) {
      const existing = await prisma.user.findUnique({ where: { telegramId } })
      if (existing) {
        return NextResponse.json(
          { error: 'Account already exists. Please login instead.' },
          { status: 409 }
        )
      }
    }
    if (email) {
      const existing = await prisma.user.findUnique({ where: { email } })
      if (existing) {
        return NextResponse.json(
          { error: 'Email already registered. Please login instead.' },
          { status: 409 }
        )
      }
    }

    const hashedPassword = password ? hashPassword(password) : null

    const user = await prisma.user.create({
      data: {
        telegramId: telegramId || null,
        email: email || null,
        password: hashedPassword,
        name: name || null,
        phone: phone || null,
      },
    })

    // Don't send password hash back to client
    const { password: _, ...safeUser } = user as any
    return NextResponse.json({ user: safeUser }, { status: 201 })
  } catch (error: any) {
    console.error('Signup error:', error)
    return NextResponse.json(
      { error: 'Signup failed: ' + error.message },
      { status: 500 }
    )
  }
}
