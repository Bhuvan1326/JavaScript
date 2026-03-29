"use client"

import { useState, useRef, useEffect, useCallback } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Loader2, Send, Brain, Calculator, Target, TrendingUp, Shield, Scale, Heart, CalendarClock, BarChart3, Sparkles } from "lucide-react"
import { parseMarkdown } from "@/lib/markdown"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  agent?: string
  timestamp: Date
}

const agentNames: Record<string, string> = {
  niveshak: "📊 Niveshak",
  karvid: "🧾 KarVid",
  yojana: "🎯 YojanaKarta",
  bazaar: "📈 BazaarGuru",
  dhan: "💪 DhanRaksha",
  vidhi: "⚖️ Vidhi",
  "life-event": "🎉 Life Event",
  "couple-planner": "💑 Couple's Planner",
  "dhan-sarthi": "🧠 DhanSarthi",
}

const agentColorMap: Record<string, string> = {
  niveshak: "from-blue-500/25 to-blue-600/15 border-blue-500/30",
  karvid: "from-green-500/25 to-green-600/15 border-green-500/30",
  yojana: "from-orange-500/25 to-orange-600/15 border-orange-500/30",
  bazaar: "from-pink-500/25 to-pink-600/15 border-pink-500/30",
  dhan: "from-red-500/25 to-red-600/15 border-red-500/30",
  vidhi: "from-slate-400/25 to-slate-500/15 border-slate-400/30",
  "life-event": "from-teal-500/25 to-teal-600/15 border-teal-500/30",
  "couple-planner": "from-rose-400/25 to-rose-500/15 border-rose-400/30",
  "dhan-sarthi": "from-purple-500/25 to-indigo-600/15 border-purple-500/30",
}

const quickPrompts = [
  { label: "Calculate my tax", icon: Calculator, color: "text-green-400 border-green-500/30 hover:bg-green-500/10" },
  { label: "FIRE planning", icon: Target, color: "text-orange-400 border-orange-500/30 hover:bg-orange-500/10" },
  { label: "Stock analysis", icon: TrendingUp, color: "text-pink-400 border-pink-500/30 hover:bg-pink-500/10" },
  { label: "Health score", icon: Shield, color: "text-red-400 border-red-500/30 hover:bg-red-500/10" },
  { label: "MF portfolio", icon: BarChart3, color: "text-blue-400 border-blue-500/30 hover:bg-blue-500/10" },
  { label: "SEBI rules", icon: Scale, color: "text-slate-300 border-slate-500/30 hover:bg-slate-500/10" },
]

export default function DhanSarthiPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "assistant",
      content: "Hello! I am **DhanSarthi**, your AI financial coordinator.\n\nI can help you with:\n• 🧾 **Tax calculations** — \"Calculate tax for 15 lakhs\"\n• 🎯 **FIRE planning** — \"What is FIRE?\" or \"My expenses are 50K\"\n• 📈 **Stock prices** — \"RELIANCE stock price\"\n• 💪 **Financial health** — \"What is my health score?\"\n• ⚖️ **Legal/Compliance** — \"What are SEBI regulations?\"\n• 🎉 **Life Events** — \"Plan for my wedding\"\n• 💑 **Couple Finance** — \"Joint budget with my partner\"\n\nWhat would you like to know?",
      agent: "dhan-sarthi",
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [backendStatus, setBackendStatus] = useState<"checking" | "online" | "offline">("checking")
  const [sessionId, setSessionId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  useEffect(() => {
    fetch("/api/dhan-sarthi")
      .then((res) => {
        if (res.ok) setBackendStatus("online")
        else setBackendStatus("offline")
      })
      .catch(() => setBackendStatus("offline"))
  }, [])

  // Load chat history on mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const storedUser = localStorage.getItem('user')
        if (!storedUser) return
        const userData = JSON.parse(storedUser)
        if (!userData.id) return
        const res = await fetch(`/api/save/chat?userId=${userData.id}&limit=50`)
        if (res.ok) {
          const data = await res.json()
          if (data.messages && data.messages.length > 0) {
            const loaded: Message[] = data.messages.map((m: any) => ({
              id: m.id,
              role: 'user' as const,
              content: m.query,
              timestamp: new Date(m.createdAt),
            })).flatMap((m: Message) => {
              const original = data.messages.find((d: any) => d.id === m.id)
              return [
                m,
                {
                  id: m.id + '-resp',
                  role: 'assistant' as const,
                  content: original?.response || '',
                  agent: original?.agentType || 'dhan-sarthi',
                  timestamp: new Date(original?.createdAt || Date.now()),
                }
              ]
            })
            if (loaded.length > 0) {
              setMessages(prev => [...prev, ...loaded])
            }
          }
        }
      } catch (e) {
        console.log('Could not load chat history:', e)
      }
    }
    loadHistory()
  }, [])

  const saveChat = useCallback(async (query: string, response: string, agentType: string) => {
    try {
      const storedUser = localStorage.getItem('user')
      if (!storedUser) return
      const userData = JSON.parse(storedUser)
      if (!userData.id) return
      await fetch('/api/save/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: userData.id, agentType, query, response }),
      })
    } catch (e) {
      console.log('Could not save chat:', e)
    }
  }, [])

  const getUserId = (): string => {
    try {
      const storedUser = localStorage.getItem('user')
      if (storedUser) {
        const userData = JSON.parse(storedUser)
        return userData.id || userData.email || 'anonymous'
      }
    } catch {}
    return 'anonymous'
  }

  const simulateStreaming = async (fullText: string, agentId: string) => {
    const newMessageId = String(Date.now() + 1)
    setMessages((prev) => [...prev, {
      id: newMessageId,
      role: "assistant",
      content: "",
      agent: agentId,
      timestamp: new Date(),
    }])
    
    const words = fullText.match(/(\S+\s+)|(\S+)/g) || [fullText]
    let currentText = ""
    
    for (let i = 0; i < words.length; i++) {
        currentText += words[i]
        setMessages((prev) => prev.map(m => 
            m.id === newMessageId ? { ...m, content: currentText } : m
        ))
        await new Promise(r => setTimeout(r, 20))
    }
  }

  const handleSend = async (customMessage?: string) => {
    const messageText = customMessage || input.trim()
    if (!messageText || loading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: messageText,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMessage])
    
    const query = messageText
    if (!customMessage) setInput("")
    setLoading(true)

    try {
      const response = await fetch("/api/bridge/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: query,
          user_id: getUserId(),
          agent_id: "dhan-sarthi",
          session_id: sessionId,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        
        if (data.session_id) {
          setSessionId(data.session_id)
        }

        const aiResponse = data.response || "I'm processing your request. Please try again."
        const agentId = data.agent || "dhan-sarthi"

        await simulateStreaming(aiResponse, agentId)
        saveChat(query, aiResponse, agentId)
      } else {
        const fallbackResponse = await fetch("/api/dhan-sarthi", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ query }),
        })

        if (fallbackResponse.ok) {
          const fallbackData = await fallbackResponse.json()
          const fallbackText = fallbackData.response || fallbackData.greeting || 
            "I'm having trouble connecting to the AI. Please try again shortly."
          
          setMessages((prev) => [...prev, {
            id: String(Date.now() + 1),
            role: "assistant",
            content: fallbackText,
            agent: "dhan-sarthi",
            timestamp: new Date(),
          }])
          saveChat(query, fallbackText, "dhan-sarthi")
        } else {
          throw new Error("Both bridge and fallback failed")
        }
      }
    } catch (error) {
      console.error('Error:', error)
      setMessages((prev) => [...prev, { 
        id: String(Date.now() + 1), 
        role: "assistant", 
        content: "Sorry, I encountered an error connecting to the AI. Please ensure the backend is running and try again.", 
        timestamp: new Date() 
      }])
    } finally {
      setLoading(false)
    }
  }

  const showQuickPrompts = messages.length <= 1

  return (
    <div className="max-w-7xl mx-auto animate-fade-in">
      {/* Page Header */}
      <div className="mb-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="p-3 bg-gradient-to-br from-purple-500 to-indigo-600 rounded-2xl shadow-lg">
              <Brain className="w-7 h-7 text-white" />
            </div>
            <span className={`absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full border-2 border-background ${backendStatus === 'online' ? 'bg-emerald-500' : backendStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500 animate-pulse'}`} />
          </div>
          <div>
            <h1 className="text-2xl font-bold flex items-center gap-2">
              DhanSarthi
              <Badge className="bg-gradient-to-r from-purple-500 to-indigo-600 border-0 text-white text-xs shadow-sm">
                <Sparkles className="w-3 h-3 mr-1" />
                AI Coordinator
              </Badge>
            </h1>
            <p className="text-sm text-muted-foreground">Your unified financial AI — routes to 9 specialist agents</p>
          </div>
        </div>
      </div>

      {/* Main Chat Container */}
      <Card className="overflow-hidden border-border/60 dark:border-border/30 shadow-2xl">
        <div className="bg-gradient-to-br from-slate-900 via-[#1a1040] to-slate-900 rounded-lg relative overflow-hidden">
          {/* Subtle background pattern */}
          <div className="absolute inset-0 opacity-[0.03]" style={{backgroundImage: 'radial-gradient(circle at 1px 1px, white 1px, transparent 0)', backgroundSize: '32px 32px'}} />
          
          <div className="h-[calc(100vh-14rem)] flex flex-col relative z-10">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-5 space-y-4">
              {messages.map((msg) => (
                <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {msg.role === 'assistant' && (
                    <div className="flex-shrink-0 mr-3 mt-1">
                      <div className={`w-8 h-8 rounded-lg bg-gradient-to-br ${agentColorMap[msg.agent || 'dhan-sarthi'] || agentColorMap['dhan-sarthi']} flex items-center justify-center text-xs border`}>
                        {msg.agent === 'dhan-sarthi' ? '🧠' : msg.agent === 'karvid' ? '🧾' : msg.agent === 'yojana' ? '🎯' : msg.agent === 'bazaar' ? '📈' : msg.agent === 'niveshak' ? '📊' : msg.agent === 'dhan' ? '💪' : msg.agent === 'vidhi' ? '⚖️' : msg.agent === 'life-event' ? '🎉' : msg.agent === 'couple-planner' ? '💑' : '🤖'}
                      </div>
                    </div>
                  )}
                  <div className={`max-w-[85%] rounded-2xl p-4 ${
                    msg.role === 'user' 
                      ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg shadow-purple-500/20' 
                      : `bg-gradient-to-br ${agentColorMap[msg.agent || 'dhan-sarthi'] || agentColorMap['dhan-sarthi']} text-white backdrop-blur-sm border`
                  }`}>
                    {msg.agent && msg.role === 'assistant' && (
                      <div className="flex items-center gap-2 mb-2 pb-2 border-b border-white/10">
                        <span className="text-xs font-semibold text-white/80">
                          {agentNames[msg.agent] || msg.agent}
                        </span>
                      </div>
                    )}
                    <div className="text-sm leading-relaxed">{parseMarkdown(msg.content)}</div>
                  </div>
                </div>
              ))}

              {loading && (
                <div className="flex justify-start">
                  <div className="flex-shrink-0 mr-3 mt-1">
                    <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500/25 to-indigo-600/15 border border-purple-500/30 flex items-center justify-center text-xs">🧠</div>
                  </div>
                  <div className="bg-gradient-to-br from-purple-500/20 to-indigo-600/10 border border-purple-500/25 backdrop-blur-sm rounded-2xl p-4 text-white flex items-center gap-3">
                    <div className="flex gap-1.5">
                      <span className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                      <span className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                      <span className="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                    </div>
                    <span className="text-sm text-purple-200/80">DhanSarthi is routing your query...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Quick Action Chips — only show at start */}
            {showQuickPrompts && (
              <div className="px-5 pb-3">
                <p className="text-xs text-white/40 mb-2 font-medium">Quick actions</p>
                <div className="flex flex-wrap gap-2">
                  {quickPrompts.map((prompt) => (
                    <button
                      key={prompt.label}
                      onClick={() => handleSend(prompt.label)}
                      disabled={loading}
                      className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium border transition-all duration-200 disabled:opacity-50 ${prompt.color}`}
                    >
                      <prompt.icon className="w-3 h-3" />
                      {prompt.label}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="p-4 border-t border-white/8 bg-black/30 backdrop-blur-sm">
              <div className="flex gap-3">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask anything about finance — taxes, FIRE, stocks, legal, couples..."
                  className="flex-1 bg-white/8 text-white rounded-xl px-4 py-3 placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-purple-500/50 border-white/10 hover:border-white/20 transition-colors"
                  disabled={loading}
                />
                <Button 
                  type="submit" 
                  disabled={loading || !input.trim()}
                  className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white px-5 py-3 rounded-xl shadow-lg shadow-purple-500/20 transition-all duration-300 disabled:opacity-40 disabled:shadow-none"
                >
                  {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
                </Button>
              </div>
            </form>
          </div>
        </div>
      </Card>
    </div>
  )
}
