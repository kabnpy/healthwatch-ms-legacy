import { ChevronRight } from "lucide-react"
import { Link } from "@tanstack/react-router"
import { Badge } from "@/components/ui/badge"

interface PolicyHeaderProps {
  clientName: string
  clientId: string
  policyNumber: string
  status: string
}

export function PolicyHeader({ clientName, clientId, policyNumber, status }: PolicyHeaderProps) {
  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-1 text-sm text-muted-foreground">
        <Link to="/clients">Clients</Link>
        <ChevronRight className="size-4" />
        <Link to="/clients/$clientId" params={{ clientId }}>{clientName}</Link>
        <ChevronRight className="size-4" />
        <span className="font-semibold text-foreground">{policyNumber}</span>
      </div>
      <div className="flex items-center gap-4">
        <h1 className="text-3xl font-bold tracking-tight">{policyNumber}</h1>
        <Badge variant={status === "Active" ? "default" : "secondary"}>
          {status}
        </Badge>
      </div>
    </div>
  )
}
