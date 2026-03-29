"use client"

import { useState, useEffect, useRef } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Send, Loader2 } from "lucide-react"
import { parseMarkdown } from "@/lib/markdown"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function VidhiPage() {
  const [disclaimers, setDisclaimers] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  // Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init",
    role: "assistant",
    content: "I am Vidhi, the Legal & Compliance agent. Do you have any questions regarding SEBI regulations, investor rights, or regulatory compliance?",
  }])
  const [input, setInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetchDisclaimers()
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const fetchDisclaimers = async () => {
    try {
      const response = await fetch("/api/vidhi")
      if (!response.ok) throw new Error("Backend error")
      const data = await response.json()
      setDisclaimers(data.disclaimers || [])
    } catch (error) {
      setDisclaimers([
        {
          title: "⚠️ Backend Offline",
          content: "Could not load disclaimers from the server.",
        },
      ])
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!input.trim() || chatLoading) return

    const query = input.trim()
    setInput("")
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
          agent_id: "vidhi"
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
          content: "Sorry, I am currently offline. Please try again later."
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

  return (
    <div className="space-y-6 pb-10">
      <div className="flex items-center gap-3">
        <span className="text-4xl">⚖️</span>
        <div>
          <h1 className="text-3xl font-bold">Vidhi</h1>
          <p className="text-muted-foreground">Compliance & Legal AI Agent</p>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="space-y-6">
          <Card className="border-blue-200 bg-blue-50">
            <CardHeader>
              <CardTitle className="text-blue-800">SEBI Compliance Information</CardTitle>
              <CardDescription className="text-blue-600">
                Important disclaimers and regulatory information you should know
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-blue-700">
                As per SEBI guidelines, we are required to display important disclaimers regarding financial advice 
                and investment recommendations. Please read through these carefully.
              </p>
            </CardContent>
          </Card>

          {loading ? (
            <div className="text-center py-8">
              <p className="text-muted-foreground">Loading disclaimers...</p>
            </div>
          ) : (
            <div className="space-y-4">
              {disclaimers.map((disclaimer, idx) => (
                <Card key={idx}>
                  <CardHeader>
                    <div className="flex items-center gap-2">
                      <Badge variant="outline">{idx + 1}</Badge>
                      <CardTitle className="text-lg">{disclaimer.title}</CardTitle>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground">{disclaimer.content}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>

        <div>
          <Card className="h-full flex flex-col border-purple-200/50 overflow-hidden pt-0">
            <CardHeader className="bg-purple-50/50 dark:bg-purple-900/20 border-b pt-4">
              <CardTitle className="flex justify-between items-center">
                <span>Ask Vidhi</span>
                <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">AI Active</Badge>
              </CardTitle>
              <CardDescription>Get instant answers about finance laws, taxes, and SEBI regulations.</CardDescription>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col p-0">
              <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[500px]">
                {messages.map((msg) => (
                  <div key={msg.id} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[85%] rounded-xl p-3 ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
                      <div className="whitespace-pre-wrap text-sm">{parseMarkdown(msg.content)}</div>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-muted rounded-xl p-3 flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="text-sm">Vidhi is analyzing regulations...</span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
              
              <div className="p-4 border-t bg-muted/30">
                <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} className="flex gap-2">
                  <Input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask a legal compliance question..."
                    disabled={chatLoading}
                    className="flex-1"
                  />
                  <Button type="submit" disabled={chatLoading || !input.trim()}>
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
