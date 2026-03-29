"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Send, Loader2, Plus, Trash2 } from "lucide-react"
import { parseMarkdown } from "@/lib/markdown"
import { useLocalStorage } from "@/hooks/use-local-storage"

interface Holding {
  name: string
  units: number
  nav: number
  sipAmount: number
  durationMonths: number
}

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function NiveshakPage() {
  const [holdings, setHoldings, hasLoaded] = useLocalStorage<Holding[]>("niveshak_holdings", [
    { name: "Parag Parikh Flexi Cap", units: 100, nav: 85.50, sipAmount: 5000, durationMonths: 12 }
  ])
  const [analyzing, setAnalyzing] = useState(false)
  const [result, setResult] = useState<any>(null)
  
  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init",
    role: "assistant",
    content: "I am Niveshak, the AI Mutual Fund Analyzer. Add your holdings to the left and click 'Analyze Portfolio' to generate statistical insights, or ask me directly to explain your risk metrics and asset allocation!",
  }])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleHoldingChange = (index: number, field: keyof Holding, value: string | number) => {
    const newHoldings = [...holdings]
    if (field === 'name') newHoldings[index].name = String(value)
    else if (field === 'units') newHoldings[index].units = parseFloat(String(value)) || 0
    else if (field === 'nav') newHoldings[index].nav = parseFloat(String(value)) || 0
    else if (field === 'sipAmount') newHoldings[index].sipAmount = parseFloat(String(value)) || 0
    else if (field === 'durationMonths') newHoldings[index].durationMonths = parseFloat(String(value)) || 0
    setHoldings(newHoldings)
  }

  const addHolding = () => {
    setHoldings([...holdings, { name: "", units: 0, nav: 0, sipAmount: 0, durationMonths: 0 }])
  }

  const removeHolding = (index: number) => {
    if (holdings.length <= 1) return
    const newHoldings = [...holdings]
    newHoldings.splice(index, 1)
    setHoldings(newHoldings)
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
          agent_id: "niveshak"
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
          content: "Sorry, the AI agent is offline."
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

  const handleAnalyze = async () => {
    const validHoldings = holdings.filter(h => h.name.trim() !== "" && h.units > 0 && h.nav > 0)
    if (validHoldings.length === 0) return
    
    setAnalyzing(true)
    try {
      const response = await fetch("/api/niveshak", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ holdings: validHoldings }),
      })

      if (response.ok) {
        const data = await response.json()
        setResult({
          totalValue: data.total_value,
          xirr: data.xirr_percent,
          sharpeRatio: data.risk_metrics?.sharpe_ratio || 0,
          holdings: data.holdings,
        })
        
        // Save for homepage dashboard
        localStorage.setItem("dashboard_portfolio", data.total_value.toString())


        // Also ping the AI
        handleSendMessage(`I just updated my portfolio analysis. I have ${validHoldings.length} funds totaling ₹${data.total_value} with an XIRR of ${data.xirr_percent}%. Can you give me a personalized review of this allocation? Note my funds: ${validHoldings.map(h => h.name).join(', ')}.`)

      } else {
        alert("Failed to analyze portfolio. Please ensure backend is running.")
      }
    } catch (e) {
      console.error(e)
    } finally {
      setAnalyzing(false)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(value)
  }

  if (!hasLoaded) return null // prevent hydration mismatch

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          📊 Niveshak 
          <Badge className="bg-blue-500 hover:bg-blue-600 text-white border-0">AI Agent Active</Badge>
        </h1>
        <p className="text-muted-foreground mt-2">
          MF Portfolio X-Ray Agent — powered by OpenClaw.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2 lg:items-start">
        {/* Form Side */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Manage Your Holdings</CardTitle>
              <CardDescription className="text-sm">
                Add the mutual funds in your portfolio to calculate dynamic XIRR performance.
                <div className="mt-3 space-y-1 text-xs opacity-90">
                  <p><b>Units:</b> Total fund quantities currently owned.</p>
                  <p><b>NAV (₹):</b> Current price per individual unit.</p>
                  <p><b>SIP (₹):</b> Your average continuous monthly deposit.</p>
                  <p><b>Months:</b> How long you've systematically invested.</p>
                </div>
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {holdings.map((holding, idx) => (
                <div key={idx} className="flex items-center gap-3 pb-3 border-b last:border-0 last:pb-0">
                  <div className="flex-1 space-y-2">
                    <Label className="text-xs text-muted-foreground">Fund Name</Label>
                    <Input 
                      placeholder="e.g. Parag Parikh Flexi Cap" 
                      value={holding.name} 
                      onChange={(e) => handleHoldingChange(idx, 'name', e.target.value)} 
                    />
                  </div>
                  <div className="w-24 space-y-2">
                    <Label className="text-xs text-muted-foreground">Units</Label>
                    <Input 
                      type="number" 
                      placeholder="0.00" 
                      value={holding.units || ''} 
                      onChange={(e) => handleHoldingChange(idx, 'units', e.target.value)} 
                    />
                  </div>
                  <div className="w-24 space-y-2">
                    <Label className="text-xs text-muted-foreground">NAV (₹)</Label>
                    <Input 
                      type="number" 
                      placeholder="0.00" 
                      value={holding.nav || ''} 
                      onChange={(e) => handleHoldingChange(idx, 'nav', e.target.value)} 
                    />
                  </div>
                  <div className="w-28 space-y-2">
                    <Label className="text-xs text-muted-foreground">SIP (₹)</Label>
                    <Input 
                      type="number" 
                      placeholder="0" 
                      value={holding.sipAmount || ''} 
                      onChange={(e) => handleHoldingChange(idx, 'sipAmount', e.target.value)} 
                    />
                  </div>
                  <div className="w-20 space-y-2">
                    <Label className="text-xs text-muted-foreground">Months</Label>
                    <Input 
                      type="number" 
                      placeholder="0" 
                      value={holding.durationMonths || ''} 
                      onChange={(e) => handleHoldingChange(idx, 'durationMonths', e.target.value)} 
                    />
                  </div>
                  <div className="pt-6">
                    <Button 
                      variant="ghost" 
                      size="icon" 
                      className="text-red-500 hover:text-red-700 hover:bg-red-100 dark:hover:bg-red-900/50"
                      onClick={() => removeHolding(idx)}
                      disabled={holdings.length <= 1}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ))}

              <Button variant="outline" className="w-full mt-2" onClick={addHolding}>
                <Plus className="w-4 h-4 mr-2" /> Add Fund
              </Button>
              
              <Button onClick={handleAnalyze} disabled={analyzing} className="w-full bg-blue-600 hover:bg-blue-700 h-11 text-base mt-4">
                {analyzing ? (
                  <><Loader2 className="w-4 h-4 mr-2 animate-spin" /> Analyzing Portfolio...</>
                ) : (
                  "Generate X-Ray Analysis"
                )}
              </Button>
            </CardContent>
          </Card>

          {result && (
            <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
              <div className="grid grid-cols-3 gap-4">
                <Card className="bg-blue-50/50 border-blue-100">
                  <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground font-medium mb-1">Total Value</p>
                    <p className="text-2xl font-bold">{formatCurrency(result.totalValue)}</p>
                  </CardContent>
                </Card>
                <Card className="bg-green-50/50 border-green-100">
                  <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground font-medium mb-1">Calculated XIRR</p>
                    <p className="text-2xl font-bold text-green-700">{result.xirr.toFixed(2)}%</p>
                  </CardContent>
                </Card>
                <Card className="bg-indigo-50/50 border-indigo-100">
                  <CardContent className="p-4">
                    <p className="text-xs text-muted-foreground font-medium mb-1">Sharpe Ratio</p>
                    <p className="text-2xl font-bold text-indigo-700">{result.sharpeRatio.toFixed(2)}</p>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}

          <Card className="border-yellow-200 bg-yellow-50">
            <CardHeader className="py-3">
              <CardTitle className="text-sm text-yellow-800">⚠️ SEBI Disclaimer</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-xs leading-relaxed text-yellow-700">
                Mutual fund investments are subject to market risks. Read all scheme-related documents carefully. 
                Past performance is not indicative of future results. This is for educational purposes only and 
                should not be construed as financial advice.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* AI Chat Sidebar */}
        <div className="lg:sticky lg:top-6">
          <Card className="h-full flex flex-col border-blue-200/50 min-h-[600px] shadow-lg overflow-hidden pt-0">
            <CardHeader className="bg-blue-50/50 dark:bg-blue-900/20 border-b pt-4">
              <CardTitle>Niveshak AI Consult</CardTitle>
              <CardDescription>Chat directly with your portfolio analyzer</CardDescription>
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
                      <span className="text-sm text-muted-foreground">Niveshak is reviewing...</span>
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
                    placeholder="Ask about large cap vs mid cap performance..."
                    disabled={chatLoading}
                    className="flex-1"
                  />
                  <Button type="submit" disabled={chatLoading || !chatInput.trim()} className="bg-blue-600 hover:bg-blue-700 text-white">
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
