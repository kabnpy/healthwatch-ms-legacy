import { BaseDocument } from "../BaseDocument"

interface CertificateTemplateProps {
  riskNote: any
  client: any
  policy: any
}

export const CertificateTemplate = ({ riskNote, client, policy }: CertificateTemplateProps) => {
  const breakdown = (riskNote.premium_breakdown as any) || {}
  
  return (
    <BaseDocument
      title="Certificate of Insurance"
      subtitle="Proof of Valid Coverage"
      documentNumber={riskNote.risk_note_number}
      date={new Date(riskNote.start_date).toLocaleDateString()}
      footerExtra={
        <div className="border-2 border-red-600 text-red-600 px-4 py-1 inline-block font-bold uppercase rotate-[-2deg] opacity-70">
          Original Document
        </div>
      }
    >
      <div className="bg-gray-100 p-6 border border-gray-300 mb-8 text-center rounded">
        <p className="text-sm italic font-serif leading-relaxed">
          "This is to certify that the insured named below is covered in
          accordance with the terms and conditions of the Master Policy, subject to
          the payment of the premium stated in the corresponding Debit Note."
        </p>
      </div>

      <div className="grid grid-cols-2 gap-12 mb-8">
        <div>
          <h2 className="text-xs font-bold uppercase border-b border-gray-300 mb-2 text-gray-500">
            The Insured:
          </h2>
          <p className="font-bold text-lg">{client.name}</p>
          <p className="text-sm text-gray-700">{client.postal_address || "N/A"}</p>
        </div>
        <div className="text-right">
          <h2 className="text-xs font-bold uppercase border-b border-gray-300 mb-2 text-gray-500">
            Policy / Contract:
          </h2>
          <p className="font-bold">{policy.policy_number}</p>
          <div className="mt-4 text-xs">
            <p className="uppercase text-gray-400 font-bold">Validity Period</p>
            <p className="font-semibold text-gray-700">From: {riskNote.start_date}</p>
            <p className="font-semibold text-gray-700">To: {riskNote.end_date}</p>
          </div>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-sm font-bold uppercase border-b-2 border-black mb-4 pb-1">
          Schedule of Benefits & Limits
        </h2>
        <table className="w-full text-sm mb-6">
          <tbody className="divide-y">
            <tr className="bg-gray-50">
              <td className="py-3 px-2 font-bold">Sum Insured</td>
              <td className="py-3 px-2 text-right font-mono font-bold">
                KES{" "}
                {breakdown?.basic
                  ? (breakdown.basic / 0.04).toLocaleString()
                  : "Refer to Policy Schedule"}
              </td>
            </tr>
            <tr>
              <td className="py-2 px-2">Authorized Passenger Liability</td>
              <td className="py-2 px-2 text-right">KES 200,000.00 Per Person</td>
            </tr>
            <tr>
              <td className="py-2 px-2">Third Party Property Damage</td>
              <td className="py-2 px-2 text-right">KES 1,000,000.00</td>
            </tr>
            <tr>
              <td className="py-2 px-2">Windscreen & Entertainment Units</td>
              <td className="py-2 px-2 text-right">KES 50,000.00</td>
            </tr>
            <tr>
              <td className="py-2 px-2">Towing & Recovery Services</td>
              <td className="py-2 px-2 text-right">KES 30,000.00</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div className="mb-8 p-4 border rounded-lg bg-gray-50/50">
        <h2 className="text-xs font-bold uppercase text-gray-500 mb-3 tracking-widest">
          Applicable Clauses & Endorsements
        </h2>
        <ul className="grid grid-cols-2 gap-x-8 gap-y-2 text-[11px] text-gray-700 list-inside list-disc font-sans uppercase">
          <li>Political Violence & Terrorism Extension</li>
          <li>Excess Protector Clause</li>
          <li>Authorized Repair Limits Clause</li>
          <li>Radio Cassette/Entertainment Limit</li>
          <li>Emergency Medical Expenses</li>
          <li>Windscreen/Glass Coverage</li>
          {riskNote.special_clauses?.map((clause: string, i: number) => (
            <li key={i}>{clause}</li>
          ))}
        </ul>
      </div>

      <div className="mt-12 flex justify-between items-end">
        <div className="text-center">
          <div className="w-48 h-1 bg-gray-200 mb-2" />
          <p className="text-[10px] uppercase text-gray-400">Insured Signature</p>
        </div>
        <div className="text-center">
          <div className="mb-2">
             {/* Placeholder for stamp/seal */}
             <div className="w-20 h-20 border-2 border-blue-800 border-dashed rounded-full flex items-center justify-center text-blue-800 text-[8px] font-bold uppercase rotate-12 opacity-40 mx-auto">
               Official Seal
             </div>
          </div>
          <p className="text-[10px] uppercase text-gray-400">Authorized Signatory</p>
        </div>
      </div>
    </BaseDocument>
  )
}
