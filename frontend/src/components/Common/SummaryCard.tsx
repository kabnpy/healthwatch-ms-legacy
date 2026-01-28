import type { LucideIcon } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { cn } from "@/lib/utils"

interface SummaryCardProps {
  title: string
  value: string | number | React.ReactNode
  icon?: LucideIcon
  description?: string
  className?: string
  valueClassName?: string
}

export function SummaryCard({
  title,
  value,
  icon: Icon,
  description,
  className,
  valueClassName,
}: SummaryCardProps) {
  return (
    <Card
      className={cn(
        "overflow-hidden transition-all hover:shadow-md",
        className,
      )}
    >
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          {title}
        </CardTitle>
        {Icon && <Icon className="h-4 w-4 text-muted-foreground/70" />}
      </CardHeader>
      <CardContent>
        <div
          className={cn("text-2xl font-bold tracking-tight", valueClassName)}
        >
          {value}
        </div>
        {description && (
          <p className="text-xs text-muted-foreground mt-1">{description}</p>
        )}
      </CardContent>
    </Card>
  )
}
