import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface AgentCardProps {
  href: string
  title: string
  description: string
  emoji: string
  features: string[]
  color?: string
}

export function AgentCard({ href, title, description, emoji, features, color = 'bg-primary/10' }: AgentCardProps) {
  return (
    <Link href={href}>
      <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
        <CardHeader>
          <div className="flex items-center gap-3">
            <div className={`text-4xl p-3 rounded-lg ${color}`}>
              {emoji}
            </div>
            <div>
              <CardTitle className="text-lg">{title}</CardTitle>
              <CardDescription>{description}</CardDescription>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {features.map((feature, i) => (
              <Badge key={i} variant="secondary">
                {feature}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
