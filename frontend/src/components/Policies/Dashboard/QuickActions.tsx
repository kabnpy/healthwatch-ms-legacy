import { FileText, PlusCircle, Printer, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface QuickActionsProps {
  onRenew: () => void
  onEndorse: () => void
  onPrintCertificate: () => void
  onPrintDebitNote: () => void
  disabled?: boolean
}

export function QuickActions({
  onRenew,
  onEndorse,
  onPrintCertificate,
  onPrintDebitNote,
  disabled = false,
}: QuickActionsProps) {
  return (
    <Card className="h-full bg-muted/20">
      <CardHeader>
        <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
          Quick Actions
        </CardTitle>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        <Button
          variant="outline"
          className="justify-start gap-2"
          onClick={onRenew}
          disabled={disabled}
        >
          <RefreshCw className="size-4" />
          Renew Policy
        </Button>
        <Button
          variant="outline"
          className="justify-start gap-2"
          onClick={onEndorse}
          disabled={disabled}
        >
          <PlusCircle className="size-4" />
          Endorse / Modify
        </Button>
        <div className="h-px bg-border my-1" />
        <Button
          variant="ghost"
          className="justify-start gap-2"
          onClick={onPrintCertificate}
          disabled={disabled}
        >
          <Printer className="size-4" />
          Print Certificate
        </Button>
        <Button
          variant="ghost"
          className="justify-start gap-2"
          onClick={onPrintDebitNote}
          disabled={disabled}
        >
          <FileText className="size-4" />
          Print Debit Note
        </Button>
      </CardContent>
    </Card>
  )
}
