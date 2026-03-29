"use client"

import { useState, useEffect } from "react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Brain, BarChart3, Calculator, Target, TrendingUp, Shield, Scale, ArrowRight, Sparkles, Wallet, PiggyBank, Activity, Heart, CalendarClock } from "lucide-react"

const agents = [
  {
    id: "dhan-sarthi",
    name: "DhanSarthi",
    emoji: "🧠",
    title: "AI Coordinator",
    description: "Ask anything! I will route your query to the right specialist automatically.",
    color: "from-purple-500 to-indigo-600",
    href: "/agents/dhan-sarthi",
    featured: true,
  },
  {
    id: "niveshak",
    name: "Niveshak",
    emoji: "📊",
    title: "MF Portfolio X-Ray",
    description: "Analyze mutual fund portfolios, calculate XIRR, Sharpe ratio, and get AI-powered insights",
    color: "from-blue-500 to-cyan-600",
    href: "/agents/niveshak",
    icon: BarChart3,
  },
  {
    id: "karvid",
    name: "KarVid",
    emoji: "🧾",
    title: "Tax Calculator",
    description: "Calculate taxes under old & new regimes, compare deductions, optimize tax savings",
    color: "from-green-500 to-emerald-600",
    href: "/agents/karvid",
    icon: Calculator,
  },
  {
    id: "yojana",
    name: "YojanaKarta",
    emoji: "🎯",
    title: "FIRE Planner",
    description: "Plan your Financial Independence, calculate FIRE number, track retirement goals",
    color: "from-orange-500 to-amber-600",
    href: "/agents/yojana",
    icon: Target,
  },
  {
    id: "bazaar",
    name: "BazaarGuru",
    emoji: "📈",
    title: "Stock Quotes",
    description: "Real-time stock quotes, market analysis, and investment recommendations",
    color: "from-pink-500 to-rose-600",
    href: "/agents/bazaar",
    icon: TrendingUp,
  },
  {
    id: "dhan",
    name: "DhanRaksha",
    emoji: "💪",
    title: "Financial Health",
    description: "Assess your financial health score, emergency fund status, savings rate analysis",
    color: "from-red-500 to-orange-600",
    href: "/agents/dhan",
    icon: Shield,
  },
  {
    id: "vidhi",
    name: "Vidhi",
    emoji: "⚖️",
    title: "Compliance",
    description: "SEBI disclaimers, regulatory information, and compliance guidelines",
    color: "from-slate-500 to-zinc-600",
    href: "/agents/vidhi",
    icon: Scale,
  },
  {
    id: "life-event",
    name: "Life Event Planner",
    emoji: "🎉",
    title: "Life Events",
    description: "Plan your finances for major milestones like marriage, education, and purchasing a home using AI",
    color: "from-teal-500 to-emerald-600",
    href: "/agents/life-event",
    icon: CalendarClock,
  },
  {
    id: "couple-planner",
    name: "Couple's Planner",
    emoji: "💑",
    title: "Joint Finances",
    description: "Plan your finances together, manage joint budgets, and achieve shared financial goals",
    color: "from-rose-400 to-pink-500",
    href: "/agents/couple-planner",
    icon: Heart,
  },
]

function AnimatedCounter({ value, prefix = "", suffix = "" }: { value: number; prefix?: string; suffix?: string }) {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    if (value <= 0) return
    const duration = 1200
    const steps = 40
    const stepValue = value / steps
    let current = 0
    const timer = setInterval(() => {
      current += stepValue
      if (current >= value) {
        setCount(value)
        clearInterval(timer)
      } else {
        setCount(Math.floor(current))
      }
    }, duration / steps)
    return () => clearInterval(timer)
  }, [value])

  if (value <= 0) return <span>—</span>

  const formatted = new Intl.NumberFormat("en-IN", {
    style: prefix === "₹" ? "currency" : "decimal",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(count)

  return <span>{prefix === "₹" ? formatted : `${formatted}${suffix}`}</span>
}

export default function Home() {
  const [user, setUser] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking")

  const [dashboardData, setDashboardData] = useState({
    portfolioValue: 0,
    taxSaved: 0,
    fireProgress: 0,
    healthScore: 0
  })

  useEffect(() => {
    const storedUser = localStorage.getItem("user")
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
    
    const loadDashboardData = () => {
      setDashboardData({
        portfolioValue: parseFloat(localStorage.getItem('dashboard_portfolio') || '0'),
        taxSaved: parseFloat(localStorage.getItem('dashboard_tax_saved') || '0'),
        fireProgress: parseFloat(localStorage.getItem('dashboard_fire') || '0'),
        healthScore: parseFloat(localStorage.getItem('dashboard_health') || '0')
      })
    }
    
    loadDashboardData()
    window.addEventListener("storage", loadDashboardData)
    
    setIsLoading(false)

    fetch("/api/dhan-sarthi")
      .then((res) => {
        if (res.ok) setBackendStatus("online")
        else setBackendStatus("offline")
      })
      .catch(() => setBackendStatus("offline"))
      
    return () => window.removeEventListener("storage", loadDashboardData)
  }, [])

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="w-10 h-10 rounded-full border-4 border-primary/30 border-t-primary animate-spin" />
      </div>
    )
  }

  return (
    <div className="space-y-10">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-purple-600 via-indigo-600 to-blue-700 p-8 md:p-14 text-white animate-fade-in">
        {/* Animated grid overlay */}
        <div className="absolute inset-0 bg-grid-white/10" />
        {/* Floating orbs */}
        <div className="absolute -top-20 -right-20 w-60 h-60 bg-purple-400/20 rounded-full blur-3xl animate-float" />
        <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-blue-400/15 rounded-full blur-3xl animate-float" style={{ animationDelay: "2s" }} />

        <div className="relative z-10">
          <div className="flex items-center gap-2 mb-5">
            <Sparkles className="w-5 h-5 animate-pulse" />
            <span className="text-sm font-medium bg-white/15 backdrop-blur-sm px-4 py-1.5 rounded-full border border-white/20">
              AI-Powered Financial Guidance
            </span>
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold mb-5 leading-tight tracking-tight">
            Your Personal
            <br />
            <span className="bg-gradient-to-r from-amber-200 via-yellow-200 to-orange-200 bg-clip-text text-transparent">
              Finance Guide
            </span>
          </h1>
          <p className="text-lg md:text-xl opacity-85 mb-8 max-w-2xl leading-relaxed">
            AI-powered financial guidance for 95% of Indians. Plan taxes, track investments, 
            achieve FIRE, and assess your financial health — all in one place.
          </p>
          <div className="flex flex-wrap gap-4">
            <Link href="/agents/dhan-sarthi">
              <Button size="lg" className="bg-white text-indigo-700 hover:bg-white/90 font-semibold shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105">
                <Brain className="w-5 h-5 mr-2" />
                Ask AI Anything
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </Link>
            <Link href={user ? "/profile" : "/login"}>
              <Button size="lg" variant="outline" className="bg-white/10 backdrop-blur-sm border-white/30 text-white hover:bg-white/20 transition-all duration-300">
                {user ? "View Profile" : "Get Started"}
              </Button>
            </Link>
          </div>
        </div>

        {/* Status Badge */}
        <div className="absolute top-5 right-5 z-20">
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium backdrop-blur-sm ${
            backendStatus === "online" 
              ? "bg-emerald-500/20 border border-emerald-400/30 text-emerald-100" 
              : backendStatus === "offline" 
              ? "bg-red-500/20 border border-red-400/30 text-red-100" 
              : "bg-yellow-500/20 border border-yellow-400/30 text-yellow-100"
          }`}>
            <span className={`w-2 h-2 rounded-full ${
              backendStatus === "online" ? "bg-emerald-400 animate-pulse" : "bg-current"
            }`} />
            {backendStatus === "checking" ? "Connecting..." : backendStatus === "online" ? "AI Online" : "Offline"}
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { icon: Wallet, label: "Portfolio Value", value: dashboardData.portfolioValue, prefix: "₹", gradient: "from-blue-500/10 to-blue-600/5 dark:from-blue-500/15 dark:to-blue-600/10", iconColor: "text-blue-600 dark:text-blue-400", textColor: "text-blue-700 dark:text-blue-300", borderColor: "border-blue-200 dark:border-blue-800" },
          { icon: PiggyBank, label: "Tax Saved", value: dashboardData.taxSaved, prefix: "₹", gradient: "from-emerald-500/10 to-emerald-600/5 dark:from-emerald-500/15 dark:to-emerald-600/10", iconColor: "text-emerald-600 dark:text-emerald-400", textColor: "text-emerald-700 dark:text-emerald-300", borderColor: "border-emerald-200 dark:border-emerald-800" },
          { icon: Target, label: "FIRE Progress", value: dashboardData.fireProgress, suffix: "%", gradient: "from-orange-500/10 to-amber-600/5 dark:from-orange-500/15 dark:to-amber-600/10", iconColor: "text-orange-600 dark:text-orange-400", textColor: "text-orange-700 dark:text-orange-300", borderColor: "border-orange-200 dark:border-orange-800" },
          { icon: Activity, label: "Health Score", value: dashboardData.healthScore, suffix: "/100", gradient: "from-purple-500/10 to-indigo-600/5 dark:from-purple-500/15 dark:to-indigo-600/10", iconColor: "text-purple-600 dark:text-purple-400", textColor: "text-purple-700 dark:text-purple-300", borderColor: "border-purple-200 dark:border-purple-800" },
        ].map((stat, i) => (
          <Card key={stat.label} className={`bg-gradient-to-br ${stat.gradient} ${stat.borderColor} card-hover animate-slide-up stagger-${i + 1}`}>
            <CardHeader className="pb-2">
              <CardDescription className={`flex items-center gap-2 ${stat.iconColor}`}>
                <stat.icon className="w-4 h-4" />
                {stat.label}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className={`text-2xl font-bold ${stat.textColor}`}>
                {user ? (
                  <AnimatedCounter value={stat.value} prefix={stat.prefix} suffix={stat.suffix} />
                ) : "—"}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Featured Agent - DhanSarthi */}
      <Card className="overflow-hidden border-2 border-purple-200 dark:border-purple-800/50 bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-purple-950/30 dark:to-indigo-950/20 animate-slide-up animate-pulse-glow">
        <div className="p-6 md:p-8">
          <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
            <div className="p-4 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl shadow-lg animate-float">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <h2 className="text-2xl font-bold">DhanSarthi</h2>
                <Badge className="bg-gradient-to-r from-purple-500 to-indigo-600 border-0 text-white shadow-sm">
                  <Sparkles className="w-3 h-3 mr-1" />
                  AI Coordinator
                </Badge>
              </div>
              <p className="text-muted-foreground mb-4">
                The brain of AI Money Mentor. Ask anything about your finances — taxes, investments, 
                retirement, stocks — and I will intelligently route your query to the right specialist.
              </p>
              <Link href="/agents/dhan-sarthi">
                <Button size="lg" className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-[1.02]">
                  <Brain className="w-5 h-5 mr-2" />
                  Start Chatting
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </Card>

      {/* Agent Cards */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold">Our AI Agents</h2>
            <p className="text-sm text-muted-foreground mt-1">9 specialists at your service</p>
          </div>
          <Link href="/agents" className="text-primary hover:underline text-sm font-medium flex items-center gap-1">
            View All <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {agents.filter(a => !a.featured).map((agent, i) => {
            const IconComponent = agent.icon
            return (
              <Link key={agent.id} href={agent.href}>
                <Card className={`h-full card-hover cursor-pointer overflow-hidden group border-border/60 dark:border-border/30 animate-slide-up stagger-${i + 1}`}>
                  <div className={`h-1.5 bg-gradient-to-r ${agent.color} transition-all duration-300 group-hover:h-2`} />
                  <CardHeader>
                    <div className="flex items-center gap-3">
                      <div className={`p-2.5 rounded-xl bg-gradient-to-br ${agent.color} text-white shadow-md transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3`}>
                        {IconComponent && <IconComponent className="w-5 h-5" />}
                      </div>
                      <div>
                        <CardTitle className="text-lg">{agent.name}</CardTitle>
                        <CardDescription>{agent.title}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-3">{agent.description}</p>
                    <div className="flex items-center text-primary text-sm font-medium group-hover:translate-x-2 transition-transform duration-300">
                      Try Now <ArrowRight className="w-4 h-4 ml-1" />
                    </div>
                  </CardContent>
                </Card>
              </Link>
            )
          })}
        </div>
      </div>

      {/* SEBI Disclaimer */}
      <Card className="border-yellow-200 dark:border-yellow-900/40 bg-yellow-50 dark:bg-yellow-950/20">
        <CardHeader>
          <CardTitle className="text-yellow-800 dark:text-yellow-400 text-sm">⚠️ SEBI Disclaimer</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-yellow-700 dark:text-yellow-300/80">
            All investments are subject to market risks. This platform provides educational information only 
            and should not be construed as financial advice. Always consult a SEBI-registered investment advisor 
            before making investment decisions.
          </p>
        </CardContent>
      </Card>
    </div>
  )
}
