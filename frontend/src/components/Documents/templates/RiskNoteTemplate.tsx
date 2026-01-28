import { BaseDocument } from "../BaseDocument"

interface RiskNoteTemplateProps {
  riskNote: any
  client: any
  policy: any
}

export const RiskNoteTemplate = ({
  riskNote,
  client,
  policy,
}: RiskNoteTemplateProps) => {
  const breakdown = (riskNote.premium_breakdown as any) || {}
  const riskItem = (riskNote.risk_item_snapshot as any) || {}

  return (
    <BaseDocument
      title="Risk Note"
      subtitle="Underwriting Transaction Summary"
      documentNumber={riskNote.risk_note_number}
      date={new Date(riskNote.start_date).toLocaleDateString()}
    >
      {/* Transaction Metadata */}
      <div className="grid grid-cols-3 gap-4 mb-8 bg-gray-50 p-4 border rounded">
        <div>
          <p className="text-[10px] uppercase text-gray-500 font-bold">
            Transaction Type
          </p>
          <p className="text-sm font-semibold">{riskNote.transaction_type}</p>
        </div>
        <div>
          <p className="text-[10px] uppercase text-gray-500 font-bold">
            Policy Number
          </p>
          <p className="text-sm font-semibold">{policy.policy_number}</p>
        </div>
        <div>
          <p className="text-[10px] uppercase text-gray-500 font-bold">
            Class of Insurance
          </p>
          <p className="text-sm font-semibold">
            {policy.product_id?.substring(0, 15)}...
          </p>
        </div>
      </div>

      {/* Insured Details */}
      <div className="mb-8">
        <h2 className="text-xs font-bold uppercase border-b border-black mb-2 pb-1">
          Insured Information
        </h2>
        <div className="grid grid-cols-2 gap-8">
          <div>
            <p className="text-lg font-bold">{client.name}</p>
            <p className="text-sm whitespace-pre-line">
              {client.postal_address || "N/A"}
            </p>
          </div>
          <div className="text-right text-sm">
            <p>
              <span className="text-gray-500">KRA PIN:</span>{" "}
              <span className="font-mono">{client.kra_pin}</span>
            </p>
            <p>
              <span className="text-gray-500">Contact:</span> {client.phone}
            </p>
          </div>
        </div>
      </div>

      {/* Risk / Asset Details */}
      <div className="mb-8">
        <h2 className="text-xs font-bold uppercase border-b border-black mb-4 pb-1">
          Risk Details / Schedule of Assets
        </h2>
        <div className="border rounded overflow-hidden">
          <table className="w-full text-xs">
            <thead className="bg-gray-100 border-b">
              <tr>
                <th className="py-2 px-3 text-left">Description</th>
                <th className="py-2 px-3 text-left">Identifier (Reg/Ref)</th>
                <th className="py-2 px-3 text-right">Sum Insured (KES)</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              <tr>
                <td className="py-3 px-3">
                  <p className="font-bold">
                    {riskItem.description || "General Cover"}
                  </p>
                  <div className="grid grid-cols-2 gap-x-4 mt-1 text-[10px] text-gray-600 uppercase">
                    {riskItem.details &&
                      Object.entries(riskItem.details).map(
                        ([key, val]: [string, any]) => (
                          <p key={key}>
                            {key}:{" "}
                            <span className="text-black font-medium">
                              {val}
                            </span>
                          </p>
                        ),
                      )}
                  </div>
                </td>
                <td className="py-3 px-3 font-mono">
                  {riskItem.identifier || "N/A"}
                </td>
                <td className="py-3 px-3 text-right font-bold">
                  {breakdown.basic
                    ? (breakdown.basic / 0.04).toLocaleString()
                    : "0.00"}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Coverage Scope */}
      <div className="mb-8">
        <h2 className="text-xs font-bold uppercase border-b border-black mb-3 pb-1">
          Scope of Cover & Special Clauses
        </h2>
        <div className="grid grid-cols-2 gap-6">
          <div className="space-y-2">
            <p className="text-[10px] font-bold text-gray-500 uppercase">
              Benefits & Limits
            </p>
            <ul className="text-[11px] list-disc list-inside space-y-1 text-gray-700">
              <li>Comprehensive insurance cover</li>
              <li>Passenger Liability included</li>
              <li>Third Party Property Damage</li>
            </ul>
          </div>
          <div className="space-y-2">
            <p className="text-[10px] font-bold text-gray-500 uppercase">
              Conditions / Warranties
            </p>
            <ul className="text-[11px] list-disc list-inside space-y-1 text-gray-700">
              {riskNote.special_clauses?.length > 0 ? (
                riskNote.special_clauses.map((c: string, i: number) => (
                  <li key={i}>{c}</li>
                ))
              ) : (
                <li>Standard policy terms and conditions apply.</li>
              )}
            </ul>
          </div>
        </div>
      </div>

      {/* Internal Premium Breakdown (Visible on Risk Note) */}
      <div className="bg-gray-50 p-4 border border-dashed rounded">
        <p className="text-[10px] font-bold text-gray-500 uppercase mb-2">
          Internal Premium Computation
        </p>
        <div className="grid grid-cols-2 gap-x-12 text-xs">
          <div className="space-y-1">
            <div className="flex justify-between">
              <span>Basic Premium</span>
              <span className="font-mono">
                {breakdown.basic?.toLocaleString()}
              </span>
            </div>
            {breakdown.extensions?.map((ext: any) => (
              <div
                key={ext.name}
                className="flex justify-between text-blue-700"
              >
                <span>+ {ext.name}</span>
                <span className="font-mono">
                  {ext.amount?.toLocaleString()}
                </span>
              </div>
            ))}
          </div>
          <div className="space-y-1 border-l pl-6 font-bold text-sm flex flex-col justify-center">
            <div className="flex justify-between border-b pb-1">
              <span>Gross Premium</span>
              <span>KES {breakdown.total?.toLocaleString()}</span>
            </div>
            <div className="flex justify-between pt-1 text-[10px] text-gray-500 font-normal italic">
              <span>Estimated Commission (12.5%)</span>
              <span>{riskNote.commission_amount?.toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>
    </BaseDocument>
  )
}
