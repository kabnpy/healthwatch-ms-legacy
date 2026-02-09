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
            <h1 className="text-2xl font-black uppercase tracking-tighter text-black">
              Debit Note
            </h1>
            <p className="text-[10px] text-slate-500 font-mono uppercase">
              Ref: {invoice.invoice_number}
            </p>
          </div>
          <div className="text-right">
            <div
              className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded border ${
                invoice.status === "Paid"
                  ? "bg-emerald-100 text-emerald-800 border-emerald-200"
                  : "bg-amber-100 text-amber-800 border-amber-200"
              }`}
            >
              {invoice.status}
            </div>
          </div>
        </div>

        {/* CORE DETAILS SECTION (Boxy Style) */}
        <div className="mt-6">
          <table className="w-full border-collapse border-x border-t border-black text-black">
            <tbody>
                <tr className="border-b border-black">
                    <th scope="row" className="w-[20%] bg-slate-50 p-3 text-[10px] font-black uppercase tracking-widest text-black border-r border-black text-left align-top">Insured</th>
                    <td className="p-3 text-[11px] align-top bg-white">
                        <div className="text-black">
                            <p className="font-bold text-base leading-tight mb-1">{client.name}</p>
                            <div className="flex justify-between items-start gap-8">
                                <p className="text-[11px] leading-relaxed">
                                    {client.postal_number ? `P.O. Box ${client.postal_number}` : "No Address Provided"}
                                    {client.postal_code && ` - ${client.postal_code}`}<br />
                                    {client.town || "Nairobi"}
                                </p>
                                <p className="font-mono text-[11px] font-bold shrink-0">
                                    P.I.N No. {client.kra_pin || "N/A"}
                                </p>
                            </div>
                        </div>
                    </td>
                </tr>
                <tr className="border-b border-black">
                    <th scope="row" className="w-[20%] bg-slate-50 p-3 text-[10px] font-black uppercase tracking-widest text-black border-r border-black text-left align-middle">Date</th>
                    <td className="p-3 text-[11px] align-middle font-bold bg-white">{yearRange}</td>
                </tr>
                <tr className="border-b border-black">
                    <th scope="row" className="w-[20%] bg-slate-50 p-3 text-[10px] font-black uppercase tracking-widest text-black border-r border-black text-left align-middle">Insurer</th>
                    <td className="p-3 text-[11px] align-middle font-bold bg-white uppercase tracking-tight">{insurerName}</td>
                </tr>
            </tbody>
          </table>
        </div>

        {/* LINE ITEMS (Multi-column list) */}
        <div className="border-x border-black bg-white overflow-hidden">
            <table className="w-full border-collapse">
                <thead>
                    <tr className="bg-slate-100 border-b border-black">
                        <th className="w-12 border-r border-black p-2 text-[9px] font-black uppercase text-center text-black">#</th>
                        <th className="border-r border-black p-2 text-[9px] font-black uppercase text-left text-black">Class of Insurance</th>
                        <th className="border-r border-black p-2 text-[9px] font-black uppercase text-left text-black">Policy No / Period</th>
                        <th className="w-32 p-2 text-[9px] font-black uppercase text-right text-black">Amount (KSH)</th>
                    </tr>
                </thead>
                <tbody>
                    {lineItems.map((item, i) => {
                        const riskNote = item.risk_note
                        const policy = riskNote?.policy
                        const product = policy?.product

                        const period = riskNote
                            ? `${new Date(riskNote.start_date).toLocaleDateString("en-GB")} - ${new Date(riskNote.end_date).toLocaleDateString("en-GB")}`
                            : "N/A"

                        return (
                            <tr key={item.id || i} className="border-b border-black last:border-b-0 bg-white">
                                <td className="border-r border-black p-2 text-[10px] text-center font-mono text-slate-600">
                                    {(i + 1).toString().padStart(2, "0")}
                                </td>
                                <td className="border-r border-black p-2 text-[11px] font-bold text-black uppercase">
                                    {product?.class_of_insurance || item.description || "N/A"}
                                </td>
                                <td className="border-r border-black p-2 text-[10px]">
                                    <div className="font-bold text-black font-mono">
                                        {policy?.policy_number || "N/A"}
                                    </div>
                                    <div className="text-slate-500 font-mono text-[9px]">
                                        {period}
                                    </div>
                                </td>
                                <td className="p-2 text-[11px] font-black text-right font-mono text-black">
                                    {(item.amount || 0).toLocaleString(undefined, {
                                        minimumFractionDigits: 2,
                                    })}
                                </td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>

        {/* FINANCIAL SUMMARY (Boxy Style) */}
        <div className="border-x border-b border-black">
            <table className="w-full border-collapse">
                <tbody>
                    <tr className="border-t border-black">
                        <th scope="row" className="w-[80%] bg-slate-50 p-2 text-[10px] font-black uppercase tracking-widest text-black border-r border-black text-right">Total Premium Payable</th>
                        <td className="p-2 text-[13px] font-black text-black text-right bg-white">
                            {formatCurrency(invoice.total_amount || 0)}
                        </td>
                    </tr>
                    {invoice.balance_due !== invoice.total_amount && (
                        <tr className="border-t border-black">
                            <th scope="row" className="w-[80%] bg-slate-50 p-2 text-[10px] font-bold uppercase tracking-widest text-red-600 border-r border-black text-right">Balance Due</th>
                            <td className="p-2 text-[13px] font-black text-red-600 text-right bg-white">
                                {formatCurrency(invoice.balance_due || 0)}
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>

        {/* PAYMENT INSTRUCTIONS (Boxy Style) */}
        <div className="mt-8 border border-black">
            <table className="w-full border-collapse">
                <tbody>
                    <tr>
                        <th scope="row" className="w-[20%] bg-slate-50 p-3 text-[10px] font-black uppercase tracking-widest text-black border-r border-black text-left align-top">Payment</th>
                        <td className="p-3 align-top bg-white">
                            <div className="grid grid-cols-2 gap-8 text-[10px] text-black">
                                <div>
                                    <p className="font-bold uppercase mb-1 border-b border-black/10 pb-1 text-black">MPESA Paybill</p>
                                    <div className="space-y-0.5 mt-2">
                                        <p>Business No: <span className="font-bold">555000</span></p>
                                        <p>Account No: <span className="font-bold font-mono">{client.kra_pin}</span></p>
                                    </div>
                                </div>
                                <div>
                                    <p className="font-bold uppercase mb-1 border-b border-black/10 pb-1 text-black">Cheque / EFT</p>
                                    <div className="space-y-0.5 mt-2">
                                        <p className="font-bold">HealthWatch Insurance Brokers Ltd</p>
                                        <p className="italic text-slate-500">Bank details available on request</p>
                                    </div>
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
      </div>
    </BaseDocument>
  )
}