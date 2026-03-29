"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Badge } from "@/components/ui/badge"
import { Loader2, Target, TrendingUp, Calculator, Info, Send } from "lucide-react"
import { toast } from "sonner"
import { parseMarkdown } from "@/lib/markdown"
import { useLocalStorage } from "@/hooks/use-local-storage"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function YojanaPage() {
  const [formData, setFormData, hasLoaded] = useLocalStorage("yojana_form", {
    monthlyExpenses: 50000,
    currentAge: 30,
    retirementAge: 50,
    currentSavings: 1000000,
    expectedReturn: 12,
    inflation: 6,
  })
  
  const [calculating, setCalculating] = useState(false)
  const [result, setResult] = useState<any>(null)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init", role: "assistant", content: "I am YojanaKarta, your FIRE (Financial Independence, Retire Early) Planner. Fill out your details below to calculate your target corpus, or chat with me to explore investment strategies like Index Funds vs Real Estate!"
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
          agent_id: "yojana"
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
          content: "Sorry, the FIRE planner agent is offline."
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

  const calculateFIRE = async () => {
    setCalculating(true)
    try {
      const response = await fetch("/api/yojana", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          monthly_expenses: formData.monthlyExpenses,
          current_age: formData.currentAge,
          retirement_age: formData.retirementAge,
          current_savings: formData.currentSavings,
          expected_return: formData.expectedReturn,
          inflation: formData.inflation,
        }),
      })
      if (!response.ok) {
        toast.error("Backend error. Please try again.")
        return
      }
      const data = await response.json()
      const fireResult = {
        fireNumber: data.fire_number || calculateFireNumber(formData.monthlyExpenses),
        inflationAdjusted: data.inflation_adjusted || calculateInflationAdjusted(formData),
        monthlySIP: data.monthly_sip || calculateMonthlySIP(formData),
        yearsToRetire: formData.retirementAge - formData.currentAge,
        currentSavings: formData.currentSavings,
        futureValueOfCurrent: data.future_value || calculateFutureValue(formData),
      }
      setResult(fireResult)
      toast.success("FIRE number calculated!")

      // Update dashboard state
      const fireProgressPercent = Math.min(100, Math.max(0, (formData.currentSavings / fireResult.fireNumber) * 100))
      localStorage.setItem('dashboard_fire', fireProgressPercent.toString())
      window.dispatchEvent(new Event("storage"))

      // AI Context Update
      handleSendMessage(`I just ran a calculation. I plan to retire in ${fireResult.yearsToRetire} years. My target inflation-adjusted corpus is ₹${formatRupees(fireResult.inflationAdjusted)} requiring a monthly SIP of ${formatCurrency(fireResult.monthlySIP)}. How feasible is this considering 12% equity returns? Can you suggest an asset allocation?`)

    } catch (error) {
      toast.error("Backend is offline. Please ensure the FastAPI server is running.")
    } finally {
      setCalculating(false)
    }
  }

  const calculateFireNumber = (monthlyExpenses: number) => monthlyExpenses * 12 * 25
  const calculateInflationAdjusted = (data: typeof formData) => {
    const fireNumber = calculateFireNumber(data.monthlyExpenses)
    return fireNumber * Math.pow(1 + data.inflation / 100, data.retirementAge - data.currentAge)
  }
  const calculateFutureValue = (data: typeof formData) => data.currentSavings * Math.pow(1 + data.expectedReturn / 100, data.retirementAge - data.currentAge)
  const calculateMonthlySIP = (data: typeof formData) => {
    const fireNumber = calculateInflationAdjusted(data)
    const futureValueOfCurrent = calculateFutureValue(data)
    const requiredFromSIP = Math.max(0, fireNumber - futureValueOfCurrent)
    const months = (data.retirementAge - data.currentAge) * 12
    const rate = data.expectedReturn / 100 / 12
    if (requiredFromSIP <= 0 || months <= 0 || rate <= 0) return 0
    return (requiredFromSIP * rate) / (Math.pow(1 + rate, months) - 1)
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency", currency: "INR", maximumFractionDigits: 0,
    }).format(value)
  }

  const formatRupees = (value: number) => {
    if (value >= 10000000) return (value / 10000000).toFixed(2) + " Cr"
    if (value >= 100000) return (value / 100000).toFixed(2) + " L"
    return value.toLocaleString("en-IN")
  }

  if (!hasLoaded) return null

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          🎯 YojanaKarta
          <Badge className="bg-orange-500 hover:bg-orange-600 text-white border-0">AI Agent Active</Badge>
        </h1>
        <p className="text-muted-foreground mt-2">
          FIRE Planner Agent. Design your path to early retirement with OpenClaw AI.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2 lg:items-start">
        {/* Form and Results Side */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Plan Your Financial Independence
              </CardTitle>
              <CardDescription>
                Calculate your FIRE number and monthly SIP to achieve financial freedom
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Monthly Expenses (₹)</Label>
                  <Input type="number" value={formData.monthlyExpenses} onChange={(e) => handleChange("monthlyExpenses", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Current Age</Label>
                  <Input type="number" value={formData.currentAge} onChange={(e) => handleChange("currentAge", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Target Retirement Age</Label>
                  <Input type="number" value={formData.retirementAge} onChange={(e) => handleChange("retirementAge", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Current Savings (₹)</Label>
                  <Input type="number" value={formData.currentSavings} onChange={(e) => handleChange("currentSavings", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Expected Return (%)</Label>
                  <Input type="number" value={formData.expectedReturn} onChange={(e) => handleChange("expectedReturn", e.target.value)} />
                </div>
                <div className="space-y-2">
                  <Label>Expected Inflation (%)</Label>
                  <Input type="number" value={formData.inflation} onChange={(e) => handleChange("inflation", e.target.value)} />
                </div>
              </div>
              <Button onClick={calculateFIRE} disabled={calculating} className="w-full bg-orange-600 hover:bg-orange-700">
                {calculating ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Calculating...</> : <><Calculator className="w-4 h-4 mr-2" /> Calculate FIRE Number</>}
              </Button>
            </CardContent>
          </Card>

          {result && (
            <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
              <div className="grid md:grid-cols-3 gap-4">
                <Card className="bg-orange-50/50 border-orange-200">
                  <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground font-medium mb-1">Base Target (4% Rule)</p>
                    <p className="text-2xl font-bold text-orange-700">₹{formatRupees(result.fireNumber)}</p>
                  </CardContent>
                </Card>
                <Card className="bg-amber-50/50 border-amber-200">
                  <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground font-medium mb-1">Target At Retirement</p>
                    <p className="text-2xl font-bold text-amber-700">₹{formatRupees(result.inflationAdjusted)}</p>
                  </CardContent>
                </Card>
                <Card className="bg-yellow-50/50 border-yellow-200">
                  <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground font-medium mb-1">Required Monthly SIP</p>
                    <p className="text-2xl font-bold text-yellow-700">{formatCurrency(result.monthlySIP)}</p>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>FIRE Journey Breakdown</CardTitle>
                  <CardDescription>How you will reach financial independence in {result.yearsToRetire} years</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center py-2">
                      <span className="text-muted-foreground">Current Savings will grow to</span>
                      <span className="font-medium font-mono">₹{formatRupees(result.futureValueOfCurrent)}</span>
                    </div>
                    <Separator />
                    <div className="flex justify-between items-center py-2">
                      <span className="text-muted-foreground">SIPs must generate remaining</span>
                      <span className="font-medium font-mono">
                        ₹{formatRupees(Math.max(0, result.inflationAdjusted - result.futureValueOfCurrent))}
                      </span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>

        {/* AI Chat Sidebar */}
        <div className="lg:sticky lg:top-6">
          <Card className="h-full flex flex-col border-orange-200/50 min-h-[600px] shadow-lg overflow-hidden pt-0">
            <CardHeader className="bg-orange-50/50 dark:bg-orange-900/20 border-b pt-4">
              <CardTitle>Yojana Consult</CardTitle>
              <CardDescription>Chat directly with your FIRE advisor</CardDescription>
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
                      <span className="text-sm text-muted-foreground">Yojana is modeling portfolios...</span>
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
                    placeholder="Ask about the 4% rule, index funds, or Safe Withdrawal Rates..."
                    disabled={chatLoading}
                    className="flex-1 border-orange-200 focus-visible:ring-orange-400"
                  />
                  <Button type="submit" disabled={chatLoading || !chatInput.trim()} className="bg-orange-600 hover:bg-orange-700 text-white">
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
