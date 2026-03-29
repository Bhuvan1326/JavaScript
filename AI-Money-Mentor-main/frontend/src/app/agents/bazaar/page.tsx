"use client"

import { useState, useRef, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Loader2, TrendingUp, Info, Send } from "lucide-react"
import { toast } from "sonner"
import { parseMarkdown } from "@/lib/markdown"
import { useLocalStorage } from "@/hooks/use-local-storage"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function BazaarPage() {
  const [symbol, setSymbol, hasLoaded] = useLocalStorage("bazaar_symbol", "")
  
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init", role: "assistant", content: "I am BazaarGuru, your AI Stock Market Analyst. Search for a stock ticker to analyze its fundamentals, or ask me directly about market trends and technical indicators!"
  }])
  const [chatInput, setChatInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

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
          agent_id: "bazaar"
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
          content: "Sorry, the Bazaar agent is offline."
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

  const searchStock = async (querySymbol?: string) => {
    const searchTarget = querySymbol || symbol
    if (!searchTarget.trim()) return
    
    setSymbol(searchTarget)
    setLoading(true)
    try {
      const response = await fetch("/api/bazaar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol: searchTarget.toUpperCase() }),
      })
      if (!response.ok) {
        setResult(null)
        toast.error("Ticker not found or API limits executed. Check your symbol.")
        return
      }
      const data = await response.json()
      setResult(data)
      toast.success(`Successfully fetched ${searchTarget}`)

      // Send context to AI
      handleSendMessage(`I just pulled up real-time quotes for ${data.name} (${data.symbol}). It is currently trading at ₹${data.price} with a P/E Ratio of ${data.pe_ratio}. Can you give me a structural analysis of this company? Should I buy, hold, or sell at this valuation?`)

    } catch (error) {
      setResult(null)
      toast.error("Backend is offline. Please ensure the FastAPI server is running.")
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 2,
    }).format(value)
  }

  const formatNumber = (value: number) => {
    if (value >= 10000000) return (value / 10000000).toFixed(2) + " Cr"
    if (value >= 100000) return (value / 100000).toFixed(2) + " L"
    return value.toLocaleString("en-IN")
  }

  if (!hasLoaded) return null

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          📈 BazaarGuru
          <Badge className="bg-pink-500 hover:bg-pink-600 text-white border-0">AI Agent Active</Badge>
        </h1>
        <p className="text-muted-foreground mt-2">
          Stock Quotes Agent — Analyze market metrics instantly with AI fundamental reviews.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2 lg:items-start">
        {/* Form and Results Side */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Search Market Database</CardTitle>
              <CardDescription>Enter NSE/BSE symbol to get real-time quotes</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex gap-4">
                <div className="flex-1 space-y-2">
                  <Label htmlFor="symbol">Stock Symbol</Label>
                  <Input
                    id="symbol"
                    placeholder="e.g., RELIANCE, TCS, INFY"
                    value={symbol}
                    onChange={(e) => setSymbol(e.target.value.toUpperCase())}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") {
                        e.preventDefault()
                        searchStock()
                      }
                    }}
                  />
                </div>
                <div className="flex items-end">
                  <Button onClick={() => searchStock()} disabled={loading || !symbol.trim()} className="bg-pink-600 hover:bg-pink-700 w-[120px]">
                    {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Get Quote"}
                  </Button>
                </div>
              </div>
              
              <div className="flex flex-wrap gap-2 pt-2">
                {["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"].map(sym => (
                  <Badge 
                    key={sym}
                    variant="outline" 
                    className="cursor-pointer hover:bg-pink-50 hover:text-pink-600 border-pink-200 transition-colors" 
                    onClick={() => searchStock(sym)}
                  >
                    {sym}
                  </Badge>
                ))}
              </div>
            </CardContent>
          </Card>

          {result && (
            <div className="space-y-6 animate-in slide-in-from-bottom-4 duration-500">
              <Card className="border-pink-200/50 shadow-md">
                <CardHeader className="bg-gradient-to-r from-pink-50/50 to-rose-50/50 border-b">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="text-xl">{result.name}</CardTitle>
                      <CardDescription className="text-sm font-medium">{result.symbol}</CardDescription>
                    </div>
                    <div className="text-right">
                      <p className="text-3xl font-bold font-mono tracking-tight">{formatCurrency(result.price)}</p>
                      <Badge className={`mt-1 ${result.change >= 0 ? "bg-green-500 hover:bg-green-600" : "bg-red-500 hover:bg-red-600"}`}>
                        {result.change >= 0 ? "▲" : "▼"} {Math.abs(result.change || 0).toFixed(2)} ({(result.change_percent || 0).toFixed(2)}%)
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                <CardContent className="pt-6">
                  <div className="grid md:grid-cols-4 gap-4">
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-xs text-muted-foreground font-medium mb-1">Day High</p>
                      <p className="text-lg font-semibold">{formatCurrency(result.high)}</p>
                    </div>
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-xs text-muted-foreground font-medium mb-1">Day Low</p>
                      <p className="text-lg font-semibold">{formatCurrency(result.low)}</p>
                    </div>
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-xs text-muted-foreground font-medium mb-1">Volume</p>
                      <p className="text-lg font-semibold">{formatNumber(result.volume)}</p>
                    </div>
                    <div className="p-4 bg-muted/40 rounded-xl border">
                      <p className="text-xs text-muted-foreground font-medium mb-1">P/E Ratio</p>
                      <p className="text-lg font-semibold font-mono">{(result.pe_ratio || 0).toFixed(2)}</p>
                    </div>
                  </div>
                  
                  <div className="mt-4 p-4 bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl border">
                    <p className="text-xs text-muted-foreground font-medium mb-1">Market Capitalization</p>
                    <p className="text-3xl font-bold text-slate-700">₹{formatNumber((result.market_cap || 0) * 10000000)}</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}
        </div>

        {/* AI Chat Sidebar */}
        <div className="lg:sticky lg:top-6">
          <Card className="h-full flex flex-col border-pink-200/50 min-h-[600px] shadow-lg overflow-hidden pt-0">
            <CardHeader className="bg-pink-50/50 dark:bg-pink-900/20 border-b pt-4">
              <CardTitle>Bazaar Consult</CardTitle>
              <CardDescription>Chat directly with your fundamental analyst</CardDescription>
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
                      <span className="text-sm text-muted-foreground">BazaarGuru is reviewing market conditions...</span>
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
                    placeholder="Ask about bullish indicators, P/E ratio meanings, or market crashes..."
                    disabled={chatLoading}
                    className="flex-1 border-pink-200 focus-visible:ring-pink-400"
                  />
                  <Button type="submit" disabled={chatLoading || !chatInput.trim()} className="bg-pink-600 hover:bg-pink-700 text-white">
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
