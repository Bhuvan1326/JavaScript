"use client"

import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Brain, BarChart3, Calculator, Target, TrendingUp, Shield, Scale, ArrowRight, Sparkles, CalendarClock, Heart } from "lucide-react"

const agents = [
  {
    id: "dhan-sarthi",
    name: "DhanSarthi",
    title: "AI Coordinator",
    description: "The brain of AI Money Mentor. Ask anything about your finances and I will intelligently route your query to the right specialist automatically.",
    features: ["Natural Language Queries", "Smart Agent Routing", "Unified Interface", "Context Awareness"],
    color: "from-purple-500 to-indigo-600",
    href: "/agents/dhan-sarthi",
    featured: true,
    icon: Brain,
  },
  {
    id: "niveshak",
    name: "Niveshak",
    title: "MF Portfolio X-Ray",
    description: "Analyze your mutual fund portfolio with AI-powered insights. Upload your CAS statement or enter holdings manually to get XIRR, Sharpe ratio, and personalized recommendations.",
    features: ["Portfolio XIRR Calculation", "Sharpe & Sortino Ratios", "Asset Allocation Analysis", "AI-Powered Recommendations"],
    color: "from-blue-500 to-cyan-600",
    href: "/agents/niveshak",
    icon: BarChart3,
  },
  {
    id: "karvid",
    name: "KarVid",
    title: "Tax Calculator",
    description: "Calculate your income tax under both old and new tax regimes. Compare deductions, optimize your tax savings, and get AI-powered tax planning advice.",
    features: ["Old vs New Regime Comparison", "Section 80C/80D Calculator", "Tax Saving Recommendations", "Capital Gains Tax"],
    color: "from-green-500 to-emerald-600",
    href: "/agents/karvid",
    icon: Calculator,
  },
  {
    id: "yojana",
    name: "YojanaKarta",
    title: "FIRE Planner",
    description: "Plan your journey to Financial Independence and Early Retirement. Calculate your FIRE number, track progress, and get personalized savings strategies.",
    features: ["FIRE Number Calculator", "Retirement Planning", "SIP Calculator", "Goal Tracking"],
    color: "from-orange-500 to-amber-600",
    href: "/agents/yojana",
    icon: Target,
  },
  {
    id: "bazaar",
    name: "BazaarGuru",
    title: "Stock Quotes",
    description: "Get real-time stock quotes, market analysis, and AI-powered investment recommendations. Track your watchlist and understand market movements.",
    features: ["Real-time Stock Prices", "Market Indices", "Technical Indicators", "AI Stock Analysis"],
    color: "from-pink-500 to-rose-600",
    href: "/agents/bazaar",
    icon: TrendingUp,
  },
  {
    id: "dhan",
    name: "DhanRaksha",
    title: "Financial Health",
    description: "Assess your overall financial health with our comprehensive questionnaire. Get a health score and actionable recommendations to improve your financial wellness.",
    features: ["Financial Health Score", "Emergency Fund Check", "Savings Rate Analysis", "Debt-to-Income Ratio"],
    color: "from-red-500 to-orange-600",
    href: "/agents/dhan",
    icon: Shield,
  },
  {
    id: "vidhi",
    name: "Vidhi",
    title: "Compliance",
    description: "Stay informed about SEBI regulations, disclaimers, and compliance requirements. Understand your rights and responsibilities as an investor.",
    features: ["SEBI Disclaimers", "Regulatory Guidelines", "Investor Rights", "Compliance Checklist"],
    color: "from-slate-500 to-zinc-600",
    href: "/agents/vidhi",
    icon: Scale,
  },
  {
    id: "life-event",
    name: "Life Event Planner",
    title: "Life Events",
    description: "Plan your finances for major milestones like marriage, education, and purchasing a home using AI.",
    features: ["Marriage Budgeting", "Education Corpus", "Home Buying ROI", "AI Generation"],
    color: "from-teal-500 to-emerald-600",
    href: "/agents/life-event",
    icon: CalendarClock,
  },
  {
    id: "couple-planner",
    name: "Couple's Planner",
    title: "Joint Finances",
    description: "Plan your finances together, manage joint budgets, and achieve shared financial goals effortlessly.",
    features: ["Split Expenses", "Joint Goal Tracking", "Debt Planning", "Shared Decisions"],
    color: "from-rose-400 to-pink-500",
    href: "/agents/couple-planner",
    icon: Heart,
  },
]

export default function AgentsPage() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-3 animate-fade-in">
        <h1 className="text-3xl md:text-4xl font-bold">
          <span className="gradient-text">AI Agent Hub</span>
        </h1>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Meet our team of specialized AI agents designed to help you with every aspect of your financial journey.
        </p>
      </div>

      {/* Featured Agent - DhanSarthi */}
      {agents.filter(a => a.featured).map((agent) => {
        const IconComponent = agent.icon
        return (
          <Card key={agent.id} className="overflow-hidden border-2 border-purple-200 dark:border-purple-800/50 bg-gradient-to-br from-purple-50 to-indigo-50 dark:from-purple-950/30 dark:to-indigo-950/20 animate-slide-up animate-pulse-glow">
            <div className="p-6 md:p-8">
              <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
                <div className="p-4 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl shadow-lg animate-float">
                  {IconComponent && <IconComponent className="w-8 h-8 text-white" />}
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h2 className="text-2xl font-bold">{agent.name}</h2>
                    <Badge className="bg-gradient-to-r from-purple-500 to-indigo-600 border-0 text-white">
                      <Sparkles className="w-3 h-3 mr-1" />
                      Featured
                    </Badge>
                  </div>
                  <p className="text-muted-foreground mb-2">{agent.title}</p>
                  <p className="text-muted-foreground mb-4">{agent.description}</p>
                  <div className="flex flex-wrap gap-2 mb-4">
                    {agent.features.map((feature, idx) => (
                      <Badge key={idx} variant="secondary" className="text-xs">{feature}</Badge>
                    ))}
                  </div>
                  <Link href={agent.href}>
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
        )
      })}

      {/* Other Agents Grid */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Specialist Agents</h2>
        <div className="grid md:grid-cols-2 gap-6">
          {agents.filter(a => !a.featured).map((agent, i) => {
            const IconComponent = agent.icon
            return (
              <Link key={agent.id} href={agent.href}>
                <Card
                  className={`h-full card-hover cursor-pointer overflow-hidden group border-border/60 dark:border-border/30 animate-slide-up stagger-${i + 1}`}
                >
                  <div className={`h-1.5 bg-gradient-to-r ${agent.color} transition-all duration-300 group-hover:h-2`} />
                  <CardHeader>
                    <div className="flex items-center gap-3">
                      <div className={`p-2.5 rounded-xl bg-gradient-to-br ${agent.color} text-white shadow-md transition-transform duration-300 group-hover:scale-110 group-hover:rotate-3`}>
                        {IconComponent && <IconComponent className="w-5 h-5" />}
                      </div>
                      <div>
                        <CardTitle>{agent.name}</CardTitle>
                        <CardDescription>{agent.title}</CardDescription>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <p className="text-sm text-muted-foreground">{agent.description}</p>
                    <div className="flex flex-wrap gap-2">
                      {agent.features.map((feature, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">{feature}</Badge>
                      ))}
                    </div>
                    <div className="pt-2 flex items-center text-primary text-sm font-medium group-hover:translate-x-2 transition-transform duration-300">
                      Try Now <ArrowRight className="w-4 h-4 ml-1" />
                    </div>
                  </CardContent>
                </Card>
              </Link>
            )
          })}
        </div>
      </div>
    </div>
  )
}
