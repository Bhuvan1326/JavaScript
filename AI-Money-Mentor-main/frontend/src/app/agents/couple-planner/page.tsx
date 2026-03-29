'use client'

import { useState, useRef, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Send, Loader2 } from 'lucide-react'
import { parseMarkdown } from '@/lib/markdown'

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function CouplePlannerPage() {
  // Person 1
  const [person1Name, setPerson1Name] = useState('Partner 1')
  const [person1Income, setPerson1Income] = useState(50000)
  const [person1Expenses, setPerson1Expenses] = useState(30000)

  // Person 2
  const [person2Name, setPerson2Name] = useState('Partner 2')
  const [person2Income, setPerson2Income] = useState(50000)
  const [person2Expenses, setPerson2Expenses] = useState(30000)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init",
    role: "assistant",
    content: "I am the Couple's Finance Planner. Fill out the joint income form or ask me directly to help plan your shared finances, budgets, and couples' SIPs!",
  }])
  const [input, setInput] = useState("")
  const [chatLoading, setChatLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messages])

  const handleSendMessage = async (customQuery?: string) => {
    const query = customQuery || input.trim()
    if (!query || chatLoading) return

    if (!customQuery) setInput("")
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
          agent_id: "couple-planner"
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
          content: "Sorry, the AI planner is offline."
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

  const handleCreatePlan = () => {
    const query = `Create a joint financial plan for ${person1Name} (Income: ₹${person1Income}, Expenses: ₹${person1Expenses}) and ${person2Name} (Income: ₹${person2Income}, Expenses: ₹${person2Expenses}). How should we split our rent and savings organically?`
    handleSendMessage(query)
  }

  return (
    <div className="container mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          💑 Couple&apos;s AI Planner
          <Badge className="bg-purple-500 hover:bg-purple-600 text-white border-0">AI Agent Active</Badge>
        </h1>
        <p className="text-muted-foreground mt-2">
          Plan your finances together using real LLM-powered dynamic analysis.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        {/* Form Column */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>👤 {person1Name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Name</Label>
                <Input value={person1Name} onChange={(e) => setPerson1Name(e.target.value)} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Income (₹)</Label>
                  <Input type="number" value={person1Income} onChange={(e) => setPerson1Income(parseFloat(e.target.value) || 0)} />
                </div>
                <div className="space-y-2">
                  <Label>Expenses (₹)</Label>
                  <Input type="number" value={person1Expenses} onChange={(e) => setPerson1Expenses(parseFloat(e.target.value) || 0)} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>👤 {person2Name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Name</Label>
                <Input value={person2Name} onChange={(e) => setPerson2Name(e.target.value)} />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Income (₹)</Label>
                  <Input type="number" value={person2Income} onChange={(e) => setPerson2Income(parseFloat(e.target.value) || 0)} />
                </div>
                <div className="space-y-2">
                  <Label>Expenses (₹)</Label>
                  <Input type="number" value={person2Expenses} onChange={(e) => setPerson2Expenses(parseFloat(e.target.value) || 0)} />
                </div>
              </div>
            </CardContent>
          </Card>

          <Button onClick={handleCreatePlan} disabled={chatLoading} className="w-full h-12 text-lg">
            {chatLoading ? "Analyzing..." : "Generate Joint AI Plan"}
          </Button>
        </div>

        {/* AI Chat Sidebar */}
        <div>
          <Card className="h-full flex flex-col border-purple-200/50 min-h-[600px] overflow-hidden pt-0">
            <CardHeader className="bg-purple-50/50 dark:bg-purple-900/20 border-b pt-4">
              <CardTitle>Plan Discussion</CardTitle>
              <CardDescription>Chat directly with the Joint Planning AI</CardDescription>
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
                      <span className="text-sm">Planner is writing...</span>
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
                    placeholder="Ask about joint accounts, splits, or shared goals..."
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