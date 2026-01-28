import type { ClientPublic, InvoicePublic } from "@/client"
import { BaseDocument } from "../BaseDocument"

interface InvoiceTemplateProps {
  invoice: InvoicePublic
  client: ClientPublic
  lineItems: any[]
}

export const InvoiceTemplate = ({
  invoice,
  client,
  lineItems,
}: InvoiceTemplateProps) => {
  return (
    <BaseDocument
      title="Debit Note / Invoice"
      subtitle="Request for Payment"
      documentNumber={invoice.invoice_number}
      date={
        invoice.date_issued
          ? new Date(invoice.date_issued).toLocaleDateString()
          : "N/A"
      }
    >
      {/* Insured Details */}
      <div className="grid grid-cols-2 gap-12 mb-8">
        <div>
          <h2 className="text-xs font-bold uppercase border-b border-gray-300 mb-2 text-gray-500">
            Bill To:
          </h2>
          <p className="font-bold text-lg">{client.name}</p>
          <p className="text-sm whitespace-pre-line text-gray-700">
            {client.postal_address || "No address provided"}
          </p>
          <p className="text-sm mt-2 font-mono">
            <span className="font-semibold font-serif">KRA PIN:</span>{" "}
            {client.kra_pin}
          </p>
        </div>
        <div className="text-right">
          <h2 className="text-xs font-bold uppercase border-b border-gray-300 mb-2 text-gray-500">
            Invoice Summary:
          </h2>
          <p className="text-sm font-semibold uppercase tracking-wider">
            Status:{" "}
            <span
              className={
                invoice.status === "Paid"
                  ? "text-green-600"
                  : "text-destructive"
              }
            >
              {invoice.status}
            </span>
          </p>
          <div className="mt-4 text-xs">
            <p className="uppercase text-gray-400 font-bold">Due Date</p>
            <p className="font-semibold text-gray-700">
              {invoice.due_date || "Upon Receipt"}
            </p>
          </div>
        </div>
      </div>

      {/* Line Items Table */}
      <div className="mb-8">
        <h2 className="text-sm font-bold uppercase border-b-2 border-black mb-4 pb-1">
          Items for Payment
        </h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b-2 border-black text-left bg-gray-50 uppercase text-[10px] tracking-widest">
              <th className="py-3 pl-2">Description / Risk Note #</th>
              <th className="py-3 pr-2 text-right">Amount (KES)</th>
            </tr>
          </thead>
          <tbody className="divide-y border-b">
            {lineItems.map((item, i) => (
              <tr key={item.id || i}>
                <td className="py-4 pl-2">
                  <p className="font-medium">{item.description}</p>
                  <p className="text-[10px] text-muted-foreground font-mono">
                    RN ID: {item.risk_note_id}
                  </p>
                </td>
                <td className="py-4 pr-2 text-right font-mono">
                  {(item.amount || 0).toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                  })}
                </td>
              </tr>
            ))}

            {/* Subtotal / Total Logic */}
            <tr className="bg-gray-50 font-bold">
              <td className="py-3 pl-2 uppercase text-xs">
                Total Invoiced Amount
              </td>
              <td className="py-3 pr-2 text-right font-mono">
                KES{" "}
                {(invoice.total_amount || 0).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </td>
            </tr>
            <tr className="bg-gray-900 text-white font-bold text-lg">
              <td className="py-4 pl-3 uppercase">Net Balance Due</td>
              <td className="py-4 pr-3 text-right font-mono">
                KES{" "}
                {(invoice.balance_due || 0).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Payment Footer */}
      <div className="mt-12 p-6 bg-blue-50/30 border-2 border-blue-100 rounded-lg">
        <h3 className="text-sm font-bold text-blue-900 mb-3 uppercase tracking-tighter">
          Payment Settlement Instructions
        </h3>
        <div className="grid grid-cols-2 gap-8 text-xs text-blue-800">
          <div className="space-y-2">
            <p className="font-bold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-400" />
              Option 1: MPESA Paybill
            </p>
            <div className="pl-4 border-l border-blue-200">
              <p>
                Business Number: <strong>555000</strong>
              </p>
              <p>
                Account Number: <strong>{client.kra_pin}</strong>
              </p>
            </div>
          </div>
          <div className="space-y-2">
            <p className="font-bold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-400" />
              Option 2: Bank Transfer / Cheque
            </p>
            <div className="pl-4 border-l border-blue-200">
              <p>
                Payable to: <strong>HealthWatch Insurance Agency</strong>
              </p>
              <p>Bank: Standard Chartered Bank, Koinange St.</p>
            </div>
          </div>
        </div>
      </div>
    </BaseDocument>
  )
}
