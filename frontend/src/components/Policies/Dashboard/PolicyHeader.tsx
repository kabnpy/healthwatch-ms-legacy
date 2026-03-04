import { RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { StatusIndicator } from "../../Common/StatusIndicator"

interface PolicyHeaderProps {
  clientName: string
  clientId: string
  policyNumber: string
  displayName?: string
  status: string
  onRenew: () => void
  onRecordRenewalInvitation: () => void
}

export function PolicyHeader({
  clientName,
  policyNumber,
  displayName,
  status,
  onRenew,
  onRecordRenewalInvitation,
}: PolicyHeaderProps) {
  return (
    <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between border-b pb-6">
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-3">
          <h1 className="text-4xl font-bold tracking-tight">
            {displayName || policyNumber}
          </h1>
          <StatusIndicator isActive={status === "Active"} label={status} />
        </div>
        <div className="flex items-center gap-2 text-sm text-muted-foreground font-medium">
          <span>{clientName}</span>
          <span className="opacity-30">•</span>
          <span className="font-mono tracking-tight">{policyNumber}</span>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          className="gap-2 h-9 px-4 font-semibold"
          onClick={onRecordRenewalInvitation}
        >
          <RefreshCw className="size-4" />
          Record Renewal Notice
        </Button>
        <Button
          variant="default"
          size="sm"
          className="gap-2 h-9 px-4 font-semibold shadow-sm"
          onClick={onRenew}
        >
          <RefreshCw className="size-4" />
          Renew
        </Button>
      </div>
    </div>
  )
}
