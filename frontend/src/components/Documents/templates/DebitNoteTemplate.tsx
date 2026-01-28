import { BaseDocument } from "../BaseDocument"

interface DebitNoteTemplateProps {
  riskNote: any
  client: any
  policy: any
}

export const DebitNoteTemplate = ({ riskNote, client, policy }: DebitNoteTemplateProps) => {
  const breakdown = (riskNote.premium_breakdown as any) || {}
  
  return (
    <BaseDocument
      title="Debit Note"
      subtitle="Insurance Premium Invoice"
      documentNumber={riskNote.risk_note_number}
      date={new Date(riskNote.start_date).toLocaleDateString()}
    >
      {/* Insured & Policy Details */}
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
            <span className="font-semibold font-serif">KRA PIN:</span> {client.kra_pin}
          </p>
        </div>
        <div className="text-right">
          <h2 className="text-xs font-bold uppercase border-b border-gray-300 mb-2 text-gray-500">
            Policy Information:
          </h2>
          <p className="font-bold text-gray-800">{policy.policy_number}</p>
          <p className="text-sm font-semibold text-primary/80 uppercase tracking-wider">{riskNote.transaction_type}</p>
          <div className="mt-4 text-xs">
            <p className="uppercase text-gray-400 font-bold">Insurance Period</p>
            <p className="font-semibold text-gray-700">{riskNote.start_date} to {riskNote.end_date}</p>
          </div>
        </div>
      </div>

      {/* Financial Table */}
      <div className="mb-8">
        <h2 className="text-sm font-bold uppercase border-b-2 border-black mb-4 pb-1">
          Premium Calculation
        </h2>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b-2 border-black text-left bg-gray-50 uppercase text-[10px] tracking-widest">
              <th className="py-3 pl-2">Description</th>
              <th className="py-3 pr-2 text-right">Amount (KES)</th>
            </tr>
          </thead>
          <tbody className="divide-y border-b">
            <tr>
              <td className="py-3 pl-2">Basic Premium</td>
              <td className="py-3 pr-2 text-right font-mono">
                {breakdown?.basic?.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                }) || "0.00"}
              </td>
            </tr>

            {breakdown?.extensions?.map((ext: any, i: number) => (
              <tr key={i} className="text-gray-700">
                <td className="py-2 pl-4 italic">• {ext.name}</td>
                <td className="py-2 pr-2 text-right font-mono">
                  {ext.amount?.toLocaleString(undefined, {
                    minimumFractionDigits: 2,
                  })}
                </td>
              </tr>
            ))}

            <tr>
              <td className="py-2 pl-2 text-gray-500">Training Levy (0.2%)</td>
              <td className="py-2 pr-2 text-right font-mono text-gray-500">
                {breakdown?.levies?.trainingLevy?.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                }) || "0.00"}
              </td>
            </tr>
            <tr>
              <td className="py-2 pl-2 text-gray-500">Policy Holders Compensation Fund (0.25%)</td>
              <td className="py-2 pr-2 text-right font-mono text-gray-500">
                {breakdown?.levies?.phcf?.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                }) || "0.00"}
              </td>
            </tr>
            <tr>
              <td className="py-2 pl-2 text-gray-500">Stamp Duty</td>
              <td className="py-2 pr-2 text-right font-mono text-gray-500">
                {breakdown?.levies?.stampDuty?.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                }) || "0.00"}
              </td>
            </tr>

            <tr className="bg-gray-900 text-white font-bold text-lg">
              <td className="py-4 pl-3">TOTAL AMOUNT PAYABLE</td>
              <td className="py-4 pr-3 text-right font-mono">
                {breakdown?.total?.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                }) || "0.00"}
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
              <p>Business Number: <strong>555000</strong></p>
              <p>Account Number: <strong>{riskNote.risk_note_number}</strong></p>
            </div>
          </div>
          <div className="space-y-2">
            <p className="font-bold flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-400" />
              Option 2: Bank Transfer / Cheque
            </p>
            <div className="pl-4 border-l border-blue-200">
              <p>Payable to: <strong>HealthWatch Insurance Agency</strong></p>
              <p>Bank: Standard Chartered Bank, Koinange St.</p>
            </div>
          </div>
        </div>
      </div>
    </BaseDocument>
  )
}
