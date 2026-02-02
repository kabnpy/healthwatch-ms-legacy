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
  const clientAny = client as any
  return (
    <BaseDocument>
      <div className="font-sans text-slate-900">
        {/* DOCUMENT HEADER */}
        <div className="flex justify-between items-end border-b-2 border-black pb-4 mb-8">
          <h1 className="text-3xl font-black uppercase tracking-tighter">
            Invoice
          </h1>
          <div className="text-right">
            <p className="text-[10px] uppercase tracking-widest text-slate-500 font-bold">
              Reference No
            </p>
            <p className="font-mono font-bold text-lg">
              {invoice.invoice_number}
            </p>
          </div>
        </div>

        {/* CLIENT DETAILS */}
        <div className="mb-10 pl-8">
          <p className="font-bold text-lg uppercase tracking-wide">
            {client.name}
          </p>
          <p className="whitespace-pre-line text-sm text-slate-700">
            {client.postal_address || "P.O. Box - N/A"}
          </p>
          <p className="text-sm text-slate-700">
            {clientAny.city || "Nairobi"}
          </p>
          <div className="mt-2 text-sm">
            <span className="font-bold text-slate-500 mr-2">PIN:</span>
            <span className="font-mono">{client.kra_pin}</span>
          </div>
        </div>

        {/* DATES */}
        <div className="flex gap-32 mb-10 pl-8">
          <div>
            <p className="font-bold text-sm mb-1 uppercase tracking-wider text-slate-500">
              Invoice Date
            </p>
            <p className="font-bold">
              {invoice.date_issued
                ? new Date(invoice.date_issued).toLocaleDateString("en-GB", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric",
                  })
                : "N/A"}
            </p>
          </div>
          <div>
            <p className="font-bold text-sm mb-1 uppercase tracking-wider text-slate-500">
              Due Date
            </p>
            <p className="font-bold">
              {invoice.due_date
                ? new Date(invoice.due_date).toLocaleDateString("en-GB", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric",
                  })
                : "Upon Receipt"}
            </p>
          </div>
        </div>

        {/* TABLE HEADER */}
        <div className="grid grid-cols-12 gap-4 border-b-2 border-black pb-2 mb-4 font-bold text-sm uppercase tracking-wider pl-4">
          <div className="col-span-1 text-center">#</div>
          <div className="col-span-8">Description / Reference</div>
          <div className="col-span-3 text-right pr-4">Amount (KES)</div>
        </div>

        {/* TABLE ROWS */}
        <div className="space-y-4 mb-8">
          {lineItems.map((item, i) => (
            <div
              key={item.id || i}
              className="grid grid-cols-12 gap-4 text-sm pl-4"
            >
              <div className="col-span-1 text-center font-bold">{i + 1}</div>
              <div className="col-span-8">
                <p className="font-bold text-base">{item.description}</p>
                {item.risk_note_id && (
                  <p className="text-xs text-slate-500 font-mono mt-1">
                    Ref: {item.risk_note_id}
                  </p>
                )}
              </div>
              <div className="col-span-3 text-right font-mono text-base pr-4">
                {(item.amount || 0).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </div>
            </div>
          ))}
        </div>

        {/* FINANCIAL BREAKDOWN */}
        <div className="mt-8 flex justify-end pr-4">
          <div className="w-1/2 max-w-sm space-y-2 text-sm">
            <div className="flex justify-between border-t-2 border-black pt-2 mt-2 text-base">
              <span className="font-bold uppercase tracking-wider">
                Total Amount
              </span>
              <span className="font-bold font-mono">
                {(invoice.total_amount || 0).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </span>
            </div>
            <div className="flex justify-between text-base text-red-600">
              <span className="font-bold uppercase tracking-wider">
                Balance Due
              </span>
              <span className="font-bold font-mono">
                {(invoice.balance_due || 0).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </span>
            </div>
          </div>
        </div>

        {/* Payment Instructions */}
        <div className="mt-12 pt-8 border-t text-xs pl-8 text-slate-600">
          <p className="font-bold uppercase text-slate-500 mb-2">
            Payment Instructions
          </p>
          <div className="grid grid-cols-2 gap-8">
            <div>
              <p className="font-bold text-black">Option 1: MPESA Paybill</p>
              <p>Business No: 555000</p>
              <p>
                Account No:{" "}
                <span className="font-mono font-bold text-black">
                  {client.kra_pin}
                </span>
              </p>
            </div>
            <div>
              <p className="font-bold text-black">Option 2: Cheque / EFT</p>
              <p>
                Payable to:{" "}
                <span className="font-bold text-black">
                  HealthWatch Insurance Brokers Ltd
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </BaseDocument>
  )
}
