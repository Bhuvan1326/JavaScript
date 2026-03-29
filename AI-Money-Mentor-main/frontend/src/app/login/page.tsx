"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Loader2, User, Mail, Phone, MessageCircle, Lock, Eye, EyeOff } from "lucide-react"
import { toast } from "sonner"

export default function LoginPage() {
  const router = useRouter()
  const [authMode, setAuthMode] = useState<"login" | "signup">("login")
  const [method, setMethod] = useState<"telegram" | "email">("email")
  const [telegramId, setTelegramId] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [name, setName] = useState("")
  const [phone, setPhone] = useState("")
  const [loading, setLoading] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (method === "telegram" && !telegramId.trim()) {
      toast.error("Please enter your Telegram ID")
      return
    }
    if (method === "email" && !email.trim()) {
      toast.error("Please enter your email")
      return
    }
    if (method === "email" && !password.trim()) {
      toast.error("Please enter your password")
      return
    }
    if (authMode === "signup" && method === "email" && password.length < 6) {
      toast.error("Password must be at least 6 characters")
      return
    }
    if (authMode === "signup" && method === "email" && !name.trim()) {
      toast.error("Please enter your name")
      return
    }
    
    setLoading(true)
    try {
      const endpoint = authMode === "login" ? "/api/auth/login" : "/api/auth/signup"
      const payload: any = {}
      if (method === "telegram") payload.telegramId = telegramId
      if (method === "email") {
        payload.email = email
        payload.password = password
      }
      if (authMode === "signup") {
        payload.name = name || (method === "telegram" ? `User_${telegramId.slice(-4)}` : email.split("@")[0])
        if (phone) payload.phone = phone
      }

      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
      const data = await response.json()

      if (!response.ok) {
        if (response.status === 404 && authMode === "login") {
          toast.error("User not found. Please sign up first.")
        } else if (response.status === 401) {
          toast.error("Incorrect password. Please try again.")
        } else if (response.status === 409) {
          toast.error(data.error || "Account already exists. Please login.")
        } else {
          toast.error(data.error || "Authentication failed")
        }
        return
      }

      const user = data.user
      localStorage.setItem("user", JSON.stringify(user))
      localStorage.setItem("isLoggedIn", "true")

      // Clear any old dashboard data for the new session
      localStorage.removeItem("dashboard_portfolio")
      localStorage.removeItem("dashboard_tax_saved")
      localStorage.removeItem("dashboard_fire")
      localStorage.removeItem("dashboard_health")

      toast.success(authMode === "login" ? "Welcome back!" : "Account created successfully!")
      setTimeout(() => window.location.href = "/", 500)
    } catch (error) {
      toast.error("Authentication failed. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-[80vh] flex items-center justify-center animate-fade-in">
      <div className="relative w-full max-w-md">
        {/* Decorative orbs */}
        <div className="absolute -top-20 -left-20 w-40 h-40 bg-purple-500/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-20 -right-20 w-40 h-40 bg-blue-500/10 rounded-full blur-3xl" />
        
        <Card className="w-full relative border-border/60 dark:border-border/30 shadow-2xl">
          <CardHeader className="text-center pb-4">
            <div className="mx-auto mb-4 w-16 h-16 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg animate-float">
              <span className="text-3xl">💰</span>
            </div>
            <CardTitle className="text-2xl">
              <span className="gradient-text">AI Money Mentor</span>
            </CardTitle>
            <CardDescription>Your personal finance guide</CardDescription>
          </CardHeader>
        <CardContent className="space-y-4">
          {/* Auth Mode Toggle */}
          <div className="flex bg-muted rounded-lg p-1">
            <button 
              className={"flex-1 py-2 text-sm font-medium rounded-md transition-colors " + (authMode === "login" ? "bg-background shadow" : "")} 
              onClick={() => setAuthMode("login")}
            >
              Login
            </button>
            <button 
              className={"flex-1 py-2 text-sm font-medium rounded-md transition-colors " + (authMode === "signup" ? "bg-background shadow" : "")} 
              onClick={() => setAuthMode("signup")}
            >
              Sign Up
            </button>
          </div>

          {/* Method Toggle */}
          <div className="flex bg-muted rounded-lg p-1">
            <button 
              className={"flex-1 py-2 text-sm font-medium rounded-md transition-colors flex items-center justify-center gap-2 " + (method === "telegram" ? "bg-background shadow" : "")} 
              onClick={() => setMethod("telegram")}
            >
              <MessageCircle className="w-4 h-4" />
              Telegram
            </button>
            <button 
              className={"flex-1 py-2 text-sm font-medium rounded-md transition-colors flex items-center justify-center gap-2 " + (method === "email" ? "bg-background shadow" : "")} 
              onClick={() => setMethod("email")}
            >
              <Mail className="w-4 h-4" />
              Email
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {authMode === "signup" && method === "email" && (
              <div className="space-y-2">
                <Label htmlFor="name">Name</Label>
                <Input id="name" type="text" placeholder="Your full name" value={name} onChange={(e) => setName(e.target.value)} required />
              </div>
            )}

            {method === "telegram" ? (
              <div className="space-y-2">
                <Label htmlFor="telegram">Telegram ID</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input id="telegram" type="text" placeholder="Enter your Telegram ID" value={telegramId} onChange={(e) => setTelegramId(e.target.value)} className="pl-10" required />
                </div>
                <p className="text-xs text-muted-foreground">Find your Telegram ID by messaging @userinfobot on Telegram</p>
              </div>
            ) : (
              <>
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input id="email" type="email" placeholder="Enter your email" value={email} onChange={(e) => setEmail(e.target.value)} className="pl-10" required />
                  </div>
                </div>
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input 
                      id="password" 
                      type={showPassword ? "text" : "password"} 
                      placeholder={authMode === "signup" ? "Create a password (min 6 chars)" : "Enter your password"} 
                      value={password} 
                      onChange={(e) => setPassword(e.target.value)} 
                      className="pl-10 pr-10" 
                      required 
                    />
                    <button 
                      type="button" 
                      onClick={() => setShowPassword(!showPassword)} 
                      className="absolute right-3 top-3 h-4 w-4 text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  </div>
                  {authMode === "signup" && (
                    <p className="text-xs text-muted-foreground">Must be at least 6 characters</p>
                  )}
                </div>
                {authMode === "signup" && (
                  <div className="space-y-2">
                    <Label htmlFor="phone">Phone (Optional)</Label>
                    <div className="relative">
                      <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input id="phone" type="tel" placeholder="+91 XXXXXXXXXX" value={phone} onChange={(e) => setPhone(e.target.value)} className="pl-10" />
                    </div>
                  </div>
                )}
              </>
            )}

            <Button type="submit" className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  {authMode === "login" ? "Logging in..." : "Creating account..."}
                </>
              ) : (
                authMode === "login" ? "Login" : "Create Account"
              )}
            </Button>
          </form>
          
          <div className="text-center text-sm text-muted-foreground">
            By continuing, you agree to our Terms of Service and Privacy Policy.
          </div>
          
          <div className="text-center">
            <Link href="/" className="text-sm text-primary hover:underline">← Back to Home</Link>
          </div>
        </CardContent>
      </Card>
      </div>
    </div>
  )
}