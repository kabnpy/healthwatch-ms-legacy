import type { ReceiptPublic, ClientPublic } from "@/client"
import { Logo } from "@/components/Common/Logo"
import { Separator } from "@/components/ui/separator"

interface ReceiptTemplateProps {
  receipt: ReceiptPublic
  client: ClientPublic
}

export function ReceiptTemplate({ receipt, client }: ReceiptTemplateProps) {
  return (
    <div className="p-8 max-w-[800px] mx-auto bg-white text-black shadow-lg rounded-sm print:shadow-none print:p-0">
      {/* Header */}
      <div className="flex justify-between items-start mb-8">
        <div className="space-y-2">
          <Logo />
          <div className="text-xs text-muted-foreground uppercase tracking-widest font-semibold pt-2">
            Official Payment Receipt
          </div>
        </div>
        <div className="text-right">
          <h1 className="text-3xl font-light text-primary">RECEIPT</h1>
          <p className="text-sm font-mono mt-1 font-bold">{receipt.receipt_number}</p>
          <p className="text-xs text-muted-foreground mt-1">Date: {receipt.date_received}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-12 mb-8">
        <div>
          <h3 className="text-[10px] font-bold uppercase text-muted-foreground mb-2">Received From:</h3>
          <p className="font-bold text-lg">{client.name}</p>
          <p className="text-sm text-muted-foreground">KRA PIN: {client.kra_pin}</p>
          <p className="text-sm text-muted-foreground whitespace-pre-line">{client.postal_address}</p>
        </div>
        <div className="text-right">
          <h3 className="text-[10px] font-bold uppercase text-muted-foreground mb-2">Payment Details:</h3>
          <p className="text-sm">Method: <span className="font-semibold">{receipt.mode}</span></p>
          <p className="text-sm">Reference: <span className="font-semibold">{receipt.reference}</span></p>
          <p className="text-sm">Status: <span className="font-semibold uppercase">{receipt.status}</span></p>
        </div>
      </div>

      <Separator className="my-6" />

      {/* Amount Section */}
      <div className="bg-primary/5 p-6 rounded-lg border-2 border-primary/10 mb-8">
        <div className="flex justify-between items-center">
          <span className="text-sm font-bold uppercase tracking-wider">Total Amount Received</span>
          <span className="text-3xl font-bold font-mono">
            KES {receipt.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}
          </span>
        </div>
      </div>

      {receipt.notes && (
        <div className="mb-8">
          <h3 className="text-[10px] font-bold uppercase text-muted-foreground mb-2">Notes:</h3>
          <p className="text-sm italic">{receipt.notes}</p>
        </div>
      )}

      {/* Footer */}
      <div className="mt-12 pt-8 border-t text-[10px] text-muted-foreground text-center space-y-1">
        <p className="font-bold">HEALTHWATCH INSURANCE BROKERS LTD</p>
        <p>This is a computer generated receipt and does not require a signature.</p>
        <p>Thank you for your payment!</p>
      </div>
    </div>
  )
}
