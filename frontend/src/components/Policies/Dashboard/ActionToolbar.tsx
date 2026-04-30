import { FileDown, Mail } from "lucide-react"
import { Button } from "@/components/ui/button"
import { ExpiryStatusLabel } from "../ExpiryStatusLabel"

interface ActionToolbarProps {
  daysToExpiry: number
  progress: string
  onDownloadPdf: () => void
  onSendInvite: () => void
  onSendReminder: () => void
  isSendingInvite: boolean
  isSendingReminder: boolean
}

export function ActionToolbar({
  daysToExpiry,
  progress,
  onDownloadPdf,
  onSendInvite,
  onSendReminder,
  isSendingInvite,
  isSendingReminder,
}: ActionToolbarProps) {
  return (
    <div className="flex flex-col md:flex-row justify-between items-start gap-6 bg-muted/30 p-6 rounded-xl border border-border/50">
      <div className="flex items-center gap-6">
        <div>
          <p className="text-[10px] text-muted-foreground uppercase font-bold tracking-widest mb-1">
            Coverage Status
          </p>
          <div className="flex items-center gap-2">
            <div
              className={`text-3xl font-bold tracking-tight ${daysToExpiry <= 0 ? "text-destructive" : ""}`}
            >
              {daysToExpiry < 0 ? "!" : daysToExpiry}
            </div>
            <div className="text-[10px] text-muted-foreground uppercase leading-tight font-semibold">
              <ExpiryStatusLabel days={daysToExpiry} />
            </div>
          </div>
        </div>
        <div className="w-32 h-1.5 bg-muted rounded-full overflow-hidden">
          <div
            className={`h-full ${daysToExpiry < 30 ? "bg-destructive" : "bg-blue-500"}`}
            style={{ width: progress }}
          />
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        <Button
          variant="outline"
          size="sm"
          className="gap-2 h-9 shadow-sm"
          onClick={onDownloadPdf}
        >
          <FileDown className="size-4" />
          Download PDF
        </Button>
        <Button
          variant="outline"
          size="sm"
          className="gap-2 h-9 shadow-sm"
          onClick={onSendInvite}
          disabled={isSendingInvite}
        >
          <Mail className="size-4" />
          {isSendingInvite ? "Sending..." : "Send Invite"}
        </Button>
        {daysToExpiry <= 7 && (
          <Button
            variant="outline"
            size="sm"
            className="gap-2 h-9 shadow-sm text-orange-600 border-orange-200 hover:bg-orange-50"
            onClick={onSendReminder}
            disabled={isSendingReminder}
          >
            <Mail className="size-4" />
            {isSendingReminder ? "Sending..." : "Send Reminder"}
          </Button>
        )}
      </div>
    </div>
  )
}
