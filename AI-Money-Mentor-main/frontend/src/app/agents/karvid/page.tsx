"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Loader2, Calculator, TrendingDown, TrendingUp, Info, Send } from "lucide-react"
import { toast } from "sonner"
import { parseMarkdown } from "@/lib/markdown"
import { useLocalStorage } from "@/hooks/use-local-storage"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function KarVidPage() {
  const [formData, setFormData, hasLoaded] = useLocalStorage("karvid_form", {
    grossIncome: 1200000,
    deductions80C: 150000,
    deductions80D: 25000,
    hra: 0,
    homeLoan: 0,
    nps: 0,
  })
  
  const [calculating, setCalculating] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [activeTab, setActiveTab] = useState("calculator")

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init", role: "assistant", content: "I am KarVid, your AI Tax Advisor for FY 2025-26 (AY 2026-27). Input your numbers in the form to generate a unified tax breakdown, or ask me directly about tax sections, exemptions, and capital gains!"
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
          agent_id: "karvid"
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
          content: "Sorry, the tax agent is offline."
        }])
      }
    } catch (e) {
      setMessages(prev => [...prev, {
        id: String(Date.now() + 1),
        role: "assistant",
        content: "Error connecting to the tax agent."
      }])
    } finally {
      setChatLoading(false)
    }
  }

  const calculateTax = async () => {
    setCalculating(true)
    try {
      const response = await fetch("/api/karvid", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          income: formData.grossIncome,
          regime: "new",
          deductions_80c: formData.deductions80C,
          deductions_80d: formData.deductions80D,
        }),
      })
      if (!response.ok) {
        toast.error("Backend error. Please try again.")
        return
      }
      const data = await response.json()
      const oldTax = data.tax_old || calculateOldRegime(formData)
      const newTax = data.tax_new || calculateNewRegime(formData.grossIncome)
      
      const oldTaxValue = oldTax?.total || oldTax
      const resObj = {
        oldRegime: oldTaxValue,
        newRegime: newTax,
        recommendation: newTax <= oldTaxValue ? "new" : "old",
        savings: Math.abs(newTax - oldTaxValue),
      }
      
      // Save for homepage dashboard
      localStorage.setItem("dashboard_tax_saved", resObj.savings.toString())

      setResult(resObj)
      toast.success("Tax calculated successfully!")
      setActiveTab("compare")

      // Inform AI of the new calculation context
      handleSendMessage(`I just calculated my income tax. I make ₹${formData.grossIncome}/year. Under the old regime, my tax is ₹${resObj.oldRegime}, and under the new regime it's ₹${resObj.newRegime}. You recommended the ${resObj.recommendation} regime saving me ₹${resObj.savings}. Do you have any personalized recommendations for me to reduce this further?`)

    } catch (error) {
      toast.error("Backend is offline. Please ensure the FastAPI server is running.")
    } finally {
      setCalculating(false)
    }
  }

  const calculateOldRegime = (data: typeof formData) => {
    const taxableIncome = Math.max(0, data.grossIncome - 50000 - data.deductions80C - data.deductions80D - data.hra - data.homeLoan - data.nps)
    let tax = 0
    if (taxableIncome > 1500000) tax = (taxableIncome - 1500000) * 0.30 + 187500
    else if (taxableIncome > 1200000) tax = (taxableIncome - 1200000) * 0.30 + 97500
    else if (taxableIncome > 900000) tax = (taxableIncome - 900000) * 0.20 + 37500
    else if (taxableIncome > 600000) tax = (taxableIncome - 600000) * 0.10 + 7500
    else if (taxableIncome > 250000) tax = (taxableIncome - 250000) * 0.05
    return { total: tax + (tax * 0.04), taxableIncome }
  }

  const calculateNewRegime = (income: number) => {
    const taxableIncome = income - 75000 // Standard deduction new regime
    let tax = 0
    if (taxableIncome > 1500000) tax = (taxableIncome - 1500000) * 0.30 + 150000
    else if (taxableIncome > 1200000) tax = (taxableIncome - 1200000) * 0.20 + 90000
    else if (taxableIncome > 900000) tax = (taxableIncome - 900000) * 0.15 + 45000
    else if (taxableIncome > 600000) tax = (taxableIncome - 600000) * 0.10 + 15000
    else if (taxableIncome > 300000) tax = (taxableIncome - 300000) * 0.05
    if (taxableIncome <= 700000) return 0 // Section 87A rebate
    return tax + (tax * 0.04)
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(value)
  }

  if (!hasLoaded) return null

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          🧾 KarVid
          <Badge className="bg-green-500 hover:bg-green-600 text-white border-0">AI Agent Active</Badge>
        </h1>
        <p className="text-muted-foreground mt-2">
          Your personal AI tax advisor. Let's optimize your tax regime dynamically.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2 lg:items-start">
        {/* Form / Charts Side */}
        <div className="space-y-6">
          <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="calculator">Tax Calculator</TabsTrigger>
              <TabsTrigger value="compare">Regime Comparison</TabsTrigger>
            </TabsList>

            <TabsContent value="calculator" className="space-y-4 mt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Income Details</CardTitle>
                  <CardDescription>Enter your income and deductions</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <Label>Gross Annual Income (₹)</Label>
                      <Input type="number" value={formData.grossIncome} onChange={(e) => handleChange("grossIncome", e.target.value)} />
                    </div>
                    <div className="space-y-2">
                      <Label>Section 80C Deductions (₹)</Label>
                      <Input type="number" value={formData.deductions80C} onChange={(e) => handleChange("deductions80C", e.target.value)} />
                      <p className="text-xs text-muted-foreground">Max: ₹1,50,000</p>
                    </div>
                    <div className="space-y-2">
                      <Label>Section 80D - Health (₹)</Label>
                      <Input type="number" value={formData.deductions80D} onChange={(e) => handleChange("deductions80D", e.target.value)} />
                      <p className="text-xs text-muted-foreground">Max: ₹25,000</p>
                    </div>
                    <div className="space-y-2">
                      <Label>NPS Contribution (₹)</Label>
                      <Input type="number" value={formData.nps} onChange={(e) => handleChange("nps", e.target.value)} />
                      <p className="text-xs text-muted-foreground">Additional ₹50,000</p>
                    </div>
                  </div>
                  <Button onClick={calculateTax} disabled={calculating} className="w-full bg-green-600 hover:bg-green-700">
                    {calculating ? <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Calculating...</> : <><Calculator className="w-4 h-4 mr-2" /> Calculate Tax</>}
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="compare" className="mt-4">
              <Card>
                <CardHeader>
                  <CardTitle>AI Regime Analysis</CardTitle>
                  <CardDescription>A visual breakdown of your tax liabilities</CardDescription>
                </CardHeader>
                <CardContent>
                  {!result ? (
                    <div className="text-center py-8">
                      <p className="text-muted-foreground mb-4">Calculate your tax first</p>
                      <Button variant="outline" onClick={() => setActiveTab("calculator")}>Go to Calculator</Button>
                    </div>
                  ) : (
                    <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
                      
                      {result.savings > 0 && (
                        <div className={`p-4 rounded-lg flex items-center gap-3 ${result.recommendation === 'new' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'}`}>
                          <Badge className={result.recommendation === 'new' ? 'bg-green-600' : 'bg-blue-600'}>
                            KARVID RECOMMENDS
                          </Badge>
                          <span className="font-semibold text-sm">
                            Switching to the {result.recommendation.toUpperCase()} regime saves you {formatCurrency(result.savings)}.
                          </span>
                        </div>
                      )}

                      {/* Visual Bar Chart Implementation */}
                      <div className="flex items-end justify-center gap-12 h-56 pt-4 border-b">
                        <div className="flex flex-col items-center justify-end h-full flex-1 max-w-[120px]">
                          <div className={`w-full rounded-t-lg relative group transition-all ${result.oldRegime <= result.newRegime ? 'bg-green-400' : 'bg-slate-300'}`}
                               style={{ height: `${Math.max(5, (result.oldRegime / Math.max(1, result.oldRegime, result.newRegime)) * 100)}%` }}>
                            <div className="absolute -top-8 w-full text-center font-bold text-sm">{formatCurrency(result.oldRegime)}</div>
                          </div>
                          <span className={`mt-4 font-semibold ${result.oldRegime <= result.newRegime ? 'text-green-700' : 'text-muted-foreground'}`}>Old Regime</span>
                        </div>

                        <div className="flex flex-col items-center justify-end h-full flex-1 max-w-[120px]">
                          <div className={`w-full rounded-t-lg relative group transition-all ${result.newRegime < result.oldRegime ? 'bg-green-400' : 'bg-slate-300'}`}
                               style={{ height: `${Math.max(5, (result.newRegime / Math.max(1, result.oldRegime, result.newRegime)) * 100)}%` }}>
                            <div className="absolute -top-8 w-full text-center font-bold text-sm">{formatCurrency(result.newRegime)}</div>
                          </div>
                          <span className={`mt-4 font-semibold ${result.newRegime < result.oldRegime ? 'text-green-700' : 'text-muted-foreground'}`}>New Regime</span>
                        </div>
                      </div>

                      <div className="flex items-start gap-2 text-xs text-muted-foreground justify-center">
                        <Info className="w-4 h-4 mt-0 flex-shrink-0" />
                        <p>Visual representation of your total tax liability.</p>
                      </div>

                    </div>
                  )}
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>

        {/* AI Chat Sidebar */}
        <div className="lg:sticky lg:top-6">
          <Card className="h-full flex flex-col border-green-200/50 min-h-[600px] shadow-lg overflow-hidden pt-0">
            <CardHeader className="bg-green-50/50 dark:bg-green-900/20 border-b pt-4">
              <CardTitle>KarVid Consult</CardTitle>
              <CardDescription>Chat directly with the Indian Tax Agent</CardDescription>
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
                      <span className="text-sm text-muted-foreground">KarVid is cross-referencing law...</span>
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
                    placeholder="Ask about 80C exemptions, HRA calculation, or capital gains..."
                    disabled={chatLoading}
                    className="flex-1 border-green-200 focus-visible:ring-green-400"
                  />
                  <Button type="submit" disabled={chatLoading || !chatInput.trim()} className="bg-green-600 hover:bg-green-700 text-white">
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
