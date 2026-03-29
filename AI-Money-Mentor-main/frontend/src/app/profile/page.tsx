'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { toast } from 'sonner'

export default function ProfilePage() {
  const router = useRouter()
  const [user, setUser] = useState<any>(null)
  const [name, setName] = useState('')
  const [phone, setPhone] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (!storedUser) {
      router.push('/login')
      return
    }
    const parsed = JSON.parse(storedUser)
    setUser(parsed)
    setName(parsed.name || '')
    setPhone(parsed.phone || '')
  }, [router])

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!user) return
    setIsLoading(true)
    try {
      const response = await fetch('/api/auth/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: user.id,
          name,
          phone,
        }),
      })
      if (response.ok) {
        const data = await response.json()
        const updatedUser = { ...user, name, phone, ...data.user }
        localStorage.setItem('user', JSON.stringify(updatedUser))
        setUser(updatedUser)
        toast.success('Profile updated!')
      } else {
        toast.error('Failed to update profile')
      }
    } catch (error) {
      console.error('Failed to update profile:', error)
      toast.error('Failed to update profile')
    } finally {
      setIsLoading(false)
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('user')
    localStorage.removeItem('isLoggedIn')
    toast.success('Logged out successfully')
    router.push('/login')
  }

  if (!user) return null

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle>Profile Settings</CardTitle>
          <CardDescription>Manage your account settings</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleUpdate} className="space-y-4">
            <div className="space-y-2">
              <Label>Telegram ID</Label>
              <Input value={user.telegramId || ''} disabled />
            </div>
            <div className="space-y-2">
              <Label>Email</Label>
              <Input value={user.email || ''} disabled />
            </div>
            <div className="space-y-2">
              <Label htmlFor="name">Name</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="phone">Phone</Label>
              <Input
                id="phone"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="Your phone number"
              />
            </div>
            <div className="flex gap-4">
              <Button type="submit" disabled={isLoading}>
                {isLoading ? 'Saving...' : 'Save Changes'}
              </Button>
              <Button type="button" variant="destructive" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
