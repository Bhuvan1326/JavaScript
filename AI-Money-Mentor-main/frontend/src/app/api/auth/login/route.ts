import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import crypto from 'crypto'

function verifyPassword(password: string, storedHash: string): boolean {
  const [salt, hash] = storedHash.split(':')
  if (!salt || !hash) return false
  const verifyHash = crypto.pbkdf2Sync(password, salt, 100000, 64, 'sha512').toString('hex')
  return hash === verifyHash
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { telegramId, email, password } = body

    if (!telegramId && !email) {
      return NextResponse.json(
        { error: 'Please provide either telegramId or email' },
        { status: 400 }
      )
    }

    let user = null
    if (telegramId) {
      user = await prisma.user.findUnique({ where: { telegramId } })
    } else if (email) {
      user = await prisma.user.findUnique({ where: { email } })
    }

    if (!user) {
      return NextResponse.json(
        { error: 'User not found. Please sign up first.' },
        { status: 404 }
      )
    }

    // Verify password for email login
    if (email && user.password) {
      if (!password) {
        return NextResponse.json(
          { error: 'Password is required' },
          { status: 400 }
        )
      }
      if (!verifyPassword(password, user.password)) {
        return NextResponse.json(
          { error: 'Incorrect password. Please try again.' },
          { status: 401 }
        )
      }
    }

    // Don't send password hash back to client
    const { password: _, ...safeUser } = user as any
    return NextResponse.json({ user: safeUser })
  } catch (error: any) {
    console.error('Login error:', error)
    return NextResponse.json(
      { error: 'Login failed: ' + error.message },
      { status: 500 }
    )
  }
}
