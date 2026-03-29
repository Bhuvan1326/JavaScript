'use client'

import { useState, useRef, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Send, Loader2 } from 'lucide-react'
import { parseMarkdown } from '@/lib/markdown'

const EVENT_TYPES = [
  { id: 'marriage', name: 'Marriage', icon: '💒', description: 'Wedding expenses' },
  { id: 'child_birth', name: 'Child Birth', icon: '👶', description: 'Hospital & initial setup' },
  { id: 'child_education', name: 'Child Education', icon: '📚', description: 'Education costs' },
  { id: 'home_purchase', name: 'Home Purchase', icon: '🏠', description: 'Down payment' },
  { id: 'car_purchase', name: 'Car Purchase', icon: '🚗', description: 'Vehicle purchase' },
  { id: 'higher_education', name: 'Higher Education', icon: '🎓', description: 'MBA, MS, PhD' },
  { id: 'retirement', name: 'Retirement', icon: '🏖️', description: 'Retirement corpus' },
  { id: 'emergency_fund', name: 'Emergency Fund', icon: '🆘', description: '6-12 months expenses' },
  { id: 'vacation', name: 'Vacation', icon: '✈️', description: 'Domestic/International' },
  { id: 'parent_care', name: 'Parent Care', icon: '👨‍👩‍👧', description: 'Medical & care expenses' },
]

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
}

export default function LifeEventPage() {
  const [eventType, setEventType] = useState('marriage')
  const [yearsUntil, setYearsUntil] = useState(5)
  const [currentCorpus, setCurrentCorpus] = useState(100000)
  const [monthlyInvestment, setMonthlyInvestment] = useState(15000)

  // AI Chat state
  const [messages, setMessages] = useState<Message[]>([{
    id: "init",
    role: "assistant",
    content: "I am your AI Life Event Planner. Select an event and fill the numbers to generate a structured AI financial plan, or ask me specific questions!",
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
          agent_id: "life-event"
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
    const eventName = EVENT_TYPES.find(e => e.id === eventType)?.name || eventType
    const query = `Create a detailed financial plan for my upcoming ${eventName} in ${yearsUntil} years. I currently have ₹${currentCorpus} saved and can invest ₹${monthlyInvestment} per month. Evaluate my shortfall and suggest asset allocations.`
    handleSendMessage(query)
  }

  return (
    <div className="container mx-auto p-6 pb-12">
      <div className="mb-8">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          Life Event AI Advisor
          <Badge className="bg-purple-500 hover:bg-purple-600 text-white border-0">AI Agent Active</Badge>
        </h1>
        <p className="text-muted-foreground mt-2">
          Plan your finances for major life events dynamically with generative AI.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Input Card */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Plan Your Life Event</CardTitle>
              <CardDescription>Select an event and timeline to get personalized AI plan</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Life Event</Label>
                <Select value={eventType} onValueChange={(v) => v && setEventType(v)}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {EVENT_TYPES.map((event) => (
                      <SelectItem key={event.id} value={event.id}>
                        <span className="flex items-center gap-2">
                          <span>{event.icon}</span>
                          <span>{event.name}</span>
                        </span>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label htmlFor="years">Years Until Event</Label>
                <Input
                  id="years"
                  type="number"
                  value={yearsUntil}
                  onChange={(e) => setYearsUntil(parseInt(e.target.value) || 0)}
                  min={1}
                  max={40}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="corpus">Current Corpus (₹)</Label>
                <Input
                  id="corpus"
                  type="number"
                  value={currentCorpus}
                  onChange={(e) => setCurrentCorpus(parseFloat(e.target.value) || 0)}
                  min={0}
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="monthly">Monthly Investment (₹)</Label>
                <Input
                  id="monthly"
                  type="number"
                  value={monthlyInvestment}
                  onChange={(e) => setMonthlyInvestment(parseFloat(e.target.value) || 0)}
                  min={0}
                />
              </div>

              <Button onClick={handleCreatePlan} disabled={chatLoading} className="w-full h-12 text-lg">
                {chatLoading ? 'Generating AI Plan...' : 'Generate AI Plan'}
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* AI Chat Sidebar */}
        <div>
          <Card className="h-full flex flex-col border-purple-200/50 min-h-[500px] overflow-hidden pt-0">
            <CardHeader className="bg-purple-50/50 dark:bg-purple-900/20 border-b pt-4">
              <CardTitle>AI Goal Discussion</CardTitle>
              <CardDescription>Chat directly with your Life Event AI</CardDescription>
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
                      <span className="text-sm">Analyzing timeline and shortfall...</span>
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
                    placeholder="Ask about inflation, SIP step-ups, or debt..."
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