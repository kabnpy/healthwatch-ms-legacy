import type { ClientPublic, InvoicePublic } from "@/client"
import { BaseDocument } from "../BaseDocument"
import { RiskNoteRow } from "./RiskNote/RiskNoteRow"

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
  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-KE", {
      style: "currency",
      currency: "KSH",
    }).format(amount)
  }

  // Calculate year range for invoice date (e.g., 2025/2026)
  const dateIssued = invoice.date_issued
    ? new Date(invoice.date_issued)
    : new Date()
  const year = dateIssued.getFullYear()
  const yearRange = `${year - 1}/${year}`

  // Get insurer from the first line item's risk note if available
  const insurerName =
    lineItems[0]?.risk_note?.policy?.product?.insurer?.name || "N/A"

  return (
    <BaseDocument>
      <div className="space-y-4">
        {/* DOCUMENT HEADER */}
        <div className="flex justify-between items-start border-b-2 border-black pb-4">
          <div>
            <h1 className="text-2xl font-black uppercase tracking-tighter">
              Debit Note
            </h1>
            <p className="text-[10px] text-gray-500 font-mono uppercase">
              Ref: {invoice.invoice_number}
            </p>
          </div>
          <div className="text-right">
            <div
              className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded ${
                invoice.status === "Paid"
                  ? "bg-green-100 text-green-800"
                  : "bg-yellow-100 text-yellow-800"
              }`}
            >
              {invoice.status}
            </div>
          </div>
        </div>

        {/* CORE DETAILS SECTION */}
        <div className="mt-6 border-t border-black">
          <RiskNoteRow
            label="Insured"
            value={
              <div className="font-bold">
                <p>{client.name}</p>
                <p className="text-[10px] text-gray-500 font-normal">
                  PIN: {client.kra_pin || "N/A"}
                </p>
                <p className="text-[10px] text-gray-500 font-normal">
                  {client.postal_address} {client.city || "Nairobi"}
                </p>
              </div>
            }
          />
          <RiskNoteRow
            label="Date"
            value={<span className="font-bold">{yearRange}</span>}
          />
          <RiskNoteRow
            label="Insurer"
            value={<span className="font-bold">{insurerName}</span>}
          />
        </div>

        {/* INSURANCE TABLE HEADER */}
        <div className="grid grid-cols-12 border-x border-b border-black bg-gray-100/50">
          <div className="col-span-1 border-r border-black p-2 text-[9px] font-black uppercase text-center">
            #
          </div>
          <div className="col-span-4 border-r border-black p-2 text-[9px] font-black uppercase">
            Class of Insurance
          </div>
          <div className="col-span-5 border-r border-black p-2 text-[9px] font-black uppercase">
            Policy No / Period
          </div>
          <div className="col-span-2 p-2 text-[9px] font-black uppercase text-right">
            Annual Premium
          </div>
        </div>

        {/* INSURANCE TABLE ROWS */}
        {lineItems.map((item, i) => {
          const riskNote = item.risk_note
          const policy = riskNote?.policy
          const product = policy?.product

          const period = riskNote
            ? `${new Date(riskNote.start_date).toLocaleDateString("en-GB")} - ${new Date(riskNote.end_date).toLocaleDateString("en-GB")}`
            : "N/A"

          return (
            <div
              key={item.id || i}
              className="grid grid-cols-12 border-x border-b border-black bg-white"
            >
              <div className="col-span-1 border-r border-black p-2 text-[10px] text-center font-mono">
                {(i + 1).toString().padStart(2, "0")}
              </div>
              <div className="col-span-4 border-r border-black p-2 text-[11px] font-bold">
                {product?.class_of_insurance || item.description || "N/A"}
              </div>
              <div className="col-span-5 border-r border-black p-2 text-[10px]">
                <div className="font-bold text-gray-900">
                  {policy?.policy_number || "N/A"}
                </div>
                <div className="text-gray-500 font-mono text-[9px]">
                  {period}
                </div>
              </div>
              <div className="col-span-2 p-2 text-[11px] font-bold text-right font-mono">
                {(item.amount || 0).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </div>
            </div>
          )
        })}

        {/* FINANCIAL SUMMARY */}
        <div className="mt-8 border-t-2 border-black pt-4">
          <div className="ml-auto w-1/2">
            <RiskNoteRow
              label="Total Premium"
              value={
                <span className="text-sm font-black">
                  {formatCurrency(invoice.total_amount || 0)}
                </span>
              }
              labelClassName="bg-gray-100"
              valueClassName="bg-gray-100"
            />
            {invoice.balance_due !== invoice.total_amount && (
              <RiskNoteRow
                label="Balance Due"
                value={
                  <span className="text-sm font-black text-red-600">
                    {formatCurrency(invoice.balance_due || 0)}
                  </span>
                }
                labelClassName="bg-transparent"
              />
            )}
          </div>
        </div>

        {/* PAYMENT INSTRUCTIONS */}
        <div className="mt-12 border-t border-black pt-4">
          <RiskNoteRow
            label="Payment"
            value={
              <div className="grid grid-cols-2 gap-4 text-[10px]">
                <div>
                  <p className="font-bold uppercase mb-1">MPESA Paybill</p>
                  <p>
                    Business No: <span className="font-bold">555000</span>
                  </p>
                  <p>
                    Account:{" "}
                    <span className="font-bold font-mono">
                      {client.kra_pin}
                    </span>
                  </p>
                </div>
                <div>
                  <p className="font-bold uppercase mb-1">Cheque / EFT</p>
                  <p>
                    Payable to:{" "}
                    <span className="font-bold">
                      HealthWatch Insurance Brokers Ltd
                    </span>
                  </p>
                </div>
              </div>
            }
          />
        </div>
      </div>
    </BaseDocument>
  )
}
