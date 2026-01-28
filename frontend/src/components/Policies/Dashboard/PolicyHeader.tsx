import { Link } from "@tanstack/react-router"
import { ChevronRight, PlusCircle, RefreshCw } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

interface PolicyHeaderProps {
  clientName: string
  clientId: string
  policyNumber: string
  status: string
  onRenew: () => void
  onEndorse: () => void
}

export function PolicyHeader({
  clientName,
  clientId,
  policyNumber,
  status,
  onRenew,
  onEndorse,
}: PolicyHeaderProps) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-1 text-sm text-muted-foreground">
          <Link to="/clients" className="hover:text-primary transition-colors">Clients</Link>
          <ChevronRight className="size-4" />
          <Link to="/clients/$clientId/overview" params={{ clientId }} className="hover:text-primary transition-colors">
            {clientName}
          </Link>
          <ChevronRight className="size-4" />
          <span className="font-semibold text-foreground">{policyNumber}</span>
        </div>
        <div className="flex items-center gap-4">
          <h1 className="text-3xl font-bold tracking-tight">{policyNumber}</h1>
          <Badge variant={status === "Active" ? "default" : "secondary"} className="h-fit">
            {status}
          </Badge>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button variant="outline" size="sm" className="gap-2" onClick={onRenew}>
          <RefreshCw className="size-4" />
          Renew
        </Button>
        <Button size="sm" className="gap-2" onClick={onEndorse}>
          <PlusCircle className="size-4" />
          Endorse
        </Button>
      </div>
    </div>
  )
}