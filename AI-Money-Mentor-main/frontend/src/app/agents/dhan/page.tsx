"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Loader2, Send } from "lucide-react"
import { parseMarkdown } from "@/lib/markdown"
import { useLocalStorage } from "@/hooks/use-local-storage"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function DhanPage() {
  const [formData, setFormData, hasLoaded] = useLocalStorage("dhan_form", {
    monthlyIncome: 100000,
    monthlyExpenses: 60000,
    emergencyFund: 200000,
    totalDebt: 500000,
    investments: 2000000,
    age: 30,
  })
  
  const [calculating, setCalculating] = useState(false)
  const [result, setResult] = useState<any>(null)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init", role: "assistant", content: "I am DhanRaksha, your Health Diagnostics AI Agent. Fill out the form to generate a unified financial health score, or ask me directly to formulate an emergency fund strategy."
  }])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleChange = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: parseFloat(value) || 0 }))
  }

  const handleSendMessage = async (customQuery?: string) => {
    const query = customQuery || chatInput.trim()
    if (!query || chatLoading) return

    if (!customQuery) setChatInput("")
    setMessages(prev => [...prev, { id: Date.now().toString(), role: "user", content: query }])
    setChatLoading(true)

    try {
      const userStr = localStorage.getItem('user')
      const userId = userStr ? JSON.parse(userStr).id : "anonymous"

      const response = await fetch("/api/bridge/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          user_id: userId,
          agent_id: "dhan"
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setMessages(prev => [...prev, {
          id: String(Date.now() + 1),
          role: "assistant",
          content: data.response || "I encountered an error analyzing that."
        }])
      } else {
        setMessages(prev => [...prev, {
          id: String(Date.now() + 1),
          role: "assistant",
          content: "Sorry, the DhanRaksha agent is offline."
        }])
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        id: String(Date.now() + 1),
        role: "assistant",
        content: "Error connecting to the AI agent."
      }])
    } finally {
      setChatLoading(false)
    }
  }

  const calculateHealthScore = async () => {
    setCalculating(true)
    try {
      const { monthlyIncome, monthlyExpenses, emergencyFund, totalDebt, investments, age } = formData
      
      const safeIncome = Math.max(1, monthlyIncome)
      const safeExpenses = Math.max(1, monthlyExpenses)
      
      const savingsRate = ((monthlyIncome - monthlyExpenses) / safeIncome) * 100
      const emergencyMonths = emergencyFund / safeExpenses
      const debtToIncome = (totalDebt / (safeIncome * 12)) * 100
      
      let score = 0
      
      if (savingsRate >= 30) score += 20
      else if (savingsRate >= 20) score += 15
      else if (savingsRate >= 10) score += 10
      else if (savingsRate >= 5) score += 5
      
      if (emergencyMonths >= 6) score += 20
      else if (emergencyMonths >= 4) score += 15
      else if (emergencyMonths >= 2) score += 10
      else if (emergencyMonths >= 1) score += 5
      
      if (debtToIncome <= 20) score += 20
      else if (debtToIncome <= 40) score += 15
      else if (debtToIncome <= 60) score += 10
      else if (debtToIncome <= 80) score += 5
      
      const investmentRatio = investments / (safeIncome * 12)
      if (investmentRatio >= 3) score += 20
      else if (investmentRatio >= 2) score += 15
      else if (investmentRatio >= 1) score += 10
      else if (investmentRatio >= 0.5) score += 5
      
      const actualMultiple = investments / (safeIncome * 12)
      if (actualMultiple >= age * 0.1) score += 20
      else if (actualMultiple >= age * 0.05) score += 15
      else if (actualMultiple >= age * 0.03) score += 10
      else if (actualMultiple >= age * 0.01) score += 5
      
      const recommendations = []
      if (savingsRate < 20) recommendations.push("Increase your savings rate to at least 20% of income")
      if (emergencyMonths < 6) recommendations.push("Build emergency fund to cover 6 months of expenses")
      if (debtToIncome > 40) recommendations.push("Focus on reducing debt before increasing investments")
      if (investmentRatio < 1) recommendations.push("Aim to have at least 1x annual income in investments")

      const finalScore = Math.min(100, score)
      
      setResult({
        overallScore: finalScore,
        savingsRate,
        emergencyMonths,
        debtToIncome,
        investmentRatio,
        recommendations,
        breakdown: {
          savings: Math.min(20, Math.floor(savingsRate / 1.5)),
          emergency: Math.min(20, Math.floor(emergencyMonths * 3.33)),
          debt: debtToIncome <= 20 ? 20 : Math.max(0, 20 - Math.floor((debtToIncome - 20) / 4)),
          investment: Math.min(20, Math.floor(investmentRatio * 6.67)),
          age: Math.min(20, Math.floor(actualMultiple / (Math.max(1, age) * 0.005))),
        }
      })

      // Update dashboard state
      localStorage.setItem('dashboard_health', finalScore.toString())
      window.dispatchEvent(new Event("storage"))

      // Alert AI context
      handleSendMessage(`I just generated my financial health score. My overall score is ${finalScore}/100. I have ${emergencyMonths.toFixed(1)} months of emergency savings, a ${debtToIncome.toFixed(1)}% Debt-to-Income ratio, and a savings rate of ${savingsRate.toFixed(1)}%. What actionable steps should I take to improve these specific bottlenecks over the next quarter?`)

    } finally {
      setCalculating(false)
    }
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-green-600"
    if (score >= 60) return "text-yellow-600"
    if (score >= 40) return "text-orange-600"
    return "text-red-600"
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return "Excellent"
    if (score >= 60) return "Good"
    if (score >= 40) return "Fair"
    return "Needs Improvement"
  }

  if (!hasLoaded) return null

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          💪 DhanRaksha
          <Badge className="bg-red-500 hover:bg-red-600 text-white border-0">AI Agent Active</Badge>
        </h1>
        <p className="text-muted-foreground mt-2">
          Diagnostic Health Agent — get personalized wellness scores.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2 lg:items-start">
        {/* Form and Results Side */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Health Assessment Form</CardTitle>
              <CardDescription>Answer a few questions to map your metrics to the AI</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Monthly Income (₹)</Label>
                  <Input type="number" value={formData.monthlyIncome} onChange={(e) => handleChange("monthlyIncome", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Monthly Expenses (₹)</Label>
                  <Input type="number" value={formData.monthlyExpenses} onChange={(e) => handleChange("monthlyExpenses", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Emergency Fund (₹)</Label>
                  <Input type="number" value={formData.emergencyFund} onChange={(e) => handleChange("emergencyFund", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Total Debt (₹)</Label>
                  <Input type="number" value={formData.totalDebt} onChange={(e) => handleChange("totalDebt", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Total Investments (₹)</Label>
                  <Input type="number" value={formData.investments} onChange={(e) => handleChange("investments", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Age</Label>
                  <Input type="number" value={formData.age} onChange={(e) => handleChange("age", e.target.value)} />
                </div>
              </div>
              <Button onClick={calculateHealthScore} disabled={calculating} className="w-full bg-red-600 hover:bg-red-700">
                {calculating ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Calculating...</> : "Generate Diagnostic"}
              </Button>
            </CardContent>
          </Card>

          {result && (
            <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
              <Card>
                <CardHeader>
                  <CardTitle>Health Score</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center mb-6">
                    <p className={`text-6xl font-bold ${getScoreColor(result.overallScore)}`}>
                      {result.overallScore}
                    </p>
                    <p className="text-xl text-muted-foreground mt-2">{getScoreLabel(result.overallScore)}</p>
                    <Progress value={result.overallScore} className="mt-4 h-3 bg-red-100" />
                  </div>

                  <div className="grid md:grid-cols-2 gap-4 mt-6">
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-sm text-muted-foreground">Savings Rate</p>
                      <p className="text-2xl font-bold">{result.savingsRate.toFixed(1)}%</p>
                      <Progress value={result.breakdown.savings * 5} className="mt-2 text-red-500" />
                    </div>
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-sm text-muted-foreground">Emergency Fund</p>
                      <p className="text-2xl font-bold">{result.emergencyMonths.toFixed(1)} mo</p>
                      <Progress value={result.breakdown.emergency * 5} className="mt-2 text-red-500" />
                    </div>
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-sm text-muted-foreground">Debt-to-Income</p>
                      <p className="text-2xl font-bold">{result.debtToIncome.toFixed(1)}%</p>
                      <Progress value={result.breakdown.debt * 5} className="mt-2 text-red-500" />
                    </div>
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-sm text-muted-foreground">Investment Ratio</p>
                      <p className="text-2xl font-bold">{result.investmentRatio.toFixed(1)}x</p>
                      <Progress value={result.breakdown.investment * 5} className="mt-2 text-red-500" />
                    </div>
                  </div>
                </CardContent>
              </Card>

              {result.recommendations.length > 0 && (
                <Card className="border-red-200 bg-red-50">
                  <CardHeader>
                    <CardTitle className="text-red-800 text-lg">💡 Areas to Improve</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2">
                      {result.recommendations.map((rec: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2 text-red-700">
                          <span className="font-bold">•</span>
                          <span className="text-sm font-medium">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </CardContent>
                </Card>
              )}
            </div>
          )}
        </div>

        {/* AI Chat Sidebar */}
        <div className="lg:sticky lg:top-6">
          <Card className="h-full flex flex-col border-red-200/50 min-h-[600px] shadow-lg overflow-hidden pt-0">
            <CardHeader className="bg-red-50/50 dark:bg-red-900/20 border-b pt-4">
              <CardTitle>DhanRaksha Consult</CardTitle>
              <CardDescription>Chat directly with your diagnostic advisor</CardDescription>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col p-0">
              <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[500px]">
                {messages.map((msg) => (
                  <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] rounded-xl p-3 ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">{parseMarkdown(msg.content)}</div>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-muted rounded-xl p-3 flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-primary" />
                      <span className="text-sm text-muted-foreground">DhanRaksha is assessing risks...</span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
              
              <div className="p-4 border-t bg-muted/30">
                <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="flex gap-2">
                  <Input
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    placeholder="Ask about debt avalanche vs snowball methods..."
                    disabled={chatLoading}
                    className="flex-1 border-red-200 focus-visible:ring-red-400"
                  />
                  <Button type="submit" disabled={chatLoading || !chatInput.trim()} className="bg-red-600 hover:bg-red-700 text-white">
                    <Send className="w-4 h-4" />
                  </Button>
                </form>
              </div>
            </CardContent>
          </Card>
        </div>

      </div>
    </div>
  )
}
