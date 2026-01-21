import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Printer } from "lucide-react"
import { Suspense } from "react"

import { RiskNotesService, PoliciesService, ClientsService } from "@/client"
import { Button } from "@/components/ui/button"
import PendingItems from "@/components/Pending/PendingItems"

function getRiskNoteQueryOptions(id: string) {
  return {
    queryFn: () => RiskNotesService.readRiskNote({ id }),
    queryKey: ["risk-notes", id],
  }
}

function getPolicyQueryOptions(policyId: string) {
  return {
    queryFn: () => PoliciesService.readPolicy({ id: policyId }),
    queryKey: ["policies", policyId],
    enabled: !!policyId,
  }
}

function getClientQueryOptions(clientId: string) {
  return {
    queryFn: () => ClientsService.readClient({ id: clientId }),
    queryKey: ["clients", clientId],
    enabled: !!clientId,
  }
}

export const Route = createFileRoute("/print/risk-notes/$id")({
  component: RiskNotePrint,
})

function RiskNotePrintContent({ id }: { id: string }) {
  const { data: riskNote } = useSuspenseQuery(getRiskNoteQueryOptions(id))
  const { data: policy } = useSuspenseQuery(getPolicyQueryOptions(riskNote.policy_id))
  const { data: client } = useSuspenseQuery(getClientQueryOptions(policy.client_id))

  return (
    <div className="max-w-[800px] mx-auto p-8 bg-white text-black min-h-screen border shadow-sm print:shadow-none print:border-none print:p-0">
      <div className="flex justify-between items-start mb-8 border-b pb-4">
        <div>
          <h1 className="text-2xl font-bold uppercase">Risk Note</h1>
          <p className="text-sm text-muted-foreground print:text-black">HealthWatch Management System</p>
        </div>
        <div className="text-right">
          <p className="font-mono text-lg font-bold">{riskNote.risk_note_number}</p>
          <p className="text-sm">Date: {new Date().toLocaleDateString()}</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-8 mb-8">
        <div>
          <h2 className="text-xs font-bold uppercase text-muted-foreground print:text-black mb-1">Client</h2>
          <p className="font-bold">{client.name}</p>
          <p className="text-sm">{client.physical_address || "No address provided"}</p>
          <p className="text-sm">KRA PIN: {client.kra_pin}</p>
        </div>
        <div className="text-right">
          <h2 className="text-xs font-bold uppercase text-muted-foreground print:text-black mb-1">Policy</h2>
          <p className="font-bold">{policy.policy_number}</p>
          <p className="text-sm">Status: {policy.status}</p>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xs font-bold uppercase text-muted-foreground print:text-black mb-2 border-b">Insurance Period</h2>
        <div className="grid grid-cols-2 gap-4">
          <p className="text-sm">From: <strong>{riskNote.start_date}</strong></p>
          <p className="text-sm">To: <strong>{riskNote.end_date}</strong></p>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-xs font-bold uppercase text-muted-foreground print:text-black mb-2 border-b">Financial Summary</h2>
        <div className="space-y-1">
          <div className="flex justify-between py-1">
            <span className="text-sm">Basic Premium</span>
            <span className="font-mono">{riskNote.basic_premium.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="flex justify-between py-1">
            <span className="text-sm">Training Levy (0.2%)</span>
            <span className="font-mono">{(riskNote.training_levy ?? 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="flex justify-between py-1">
            <span className="text-sm">PHCF Levy (0.25%)</span>
            <span className="font-mono">{(riskNote.phcf_levy ?? 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="flex justify-between py-1">
            <span className="text-sm">Stamp Duty</span>
            <span className="font-mono">{(riskNote.stamp_duty ?? 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="flex justify-between py-2 border-t-2 border-black font-bold text-lg mt-2">
            <span>TOTAL PAYABLE</span>
            <span className="font-mono">KES {riskNote.gross_premium.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
          </div>
        </div>
      </div>

      {riskNote.special_clauses && riskNote.special_clauses.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xs font-bold uppercase text-muted-foreground print:text-black mb-2 border-b">Special Clauses</h2>
          <ul className="list-disc list-inside text-sm space-y-1">
            {riskNote.special_clauses.map((clause, i) => (
              <li key={i}>{clause}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-16 pt-8 border-t text-center text-[10px] text-muted-foreground print:text-black">
        <p>This is a computer generated document and does not require a signature.</p>
        <p>Generated by HealthWatch MS on {new Date().toLocaleString()}</p>
      </div>

      <div className="fixed bottom-8 right-8 print:hidden">
        <Button onClick={() => window.print()} size="lg" className="shadow-xl rounded-full gap-2">
          <Printer className="size-5" />
          Print Document
        </Button>
      </div>
    </div>
  )
}

function RiskNotePrint() {
  const { id } = Route.useParams()

  return (
    <div className="bg-muted/50 min-h-screen print:bg-white">
      <Suspense fallback={<PendingItems />}>
        <RiskNotePrintContent id={id} />
      </Suspense>
    </div>
  )
}
