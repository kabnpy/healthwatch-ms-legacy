import { useSuspenseQuery } from "@tanstack/react-query"
import { ClientsService, PoliciesService, RiskNotesService } from "@/client"
import { Button } from "@/components/ui/button"
import { CertificateTemplate } from "./templates/CertificateTemplate"
import { DebitNoteTemplate } from "./templates/DebitNoteTemplate"

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

interface RiskNoteDocumentProps {
  id: string
  mode: "invoice" | "certificate"
  onModeChange: (mode: "invoice" | "certificate") => void
}

/**
 * Controller for Risk Note based documents.
 * Dispatches to the appropriate template based on 'mode'.
 */
export function RiskNoteDocument({
  id,
  mode,
  onModeChange,
}: RiskNoteDocumentProps) {
  const { data: riskNote } = useSuspenseQuery(getRiskNoteQueryOptions(id))
  const { data: policy } = useSuspenseQuery(
    getPolicyQueryOptions(riskNote.policy_id),
  )
  const { data: client } = useSuspenseQuery(
    getClientQueryOptions(policy.client_id),
  )

  const isInvoice = mode === "invoice"

  return (
    <div className="relative group">
      {/* Document Toggle Controls (Overlay) */}
      <div className="absolute top-4 right-4 print:hidden flex flex-col gap-2 z-50">
        <div className="flex bg-white/90 backdrop-blur-sm rounded-lg shadow-xl overflow-hidden border p-1 scale-90 origin-top-right transition-all hover:scale-100">
          <Button
            variant={isInvoice ? "secondary" : "ghost"}
            className="rounded-none h-8 text-xs font-bold"
            onClick={() => onModeChange("invoice")}
          >
            DEBIT NOTE
          </Button>
          <Button
            variant={!isInvoice ? "secondary" : "ghost"}
            className="rounded-none h-8 text-xs font-bold"
            onClick={() => onModeChange("certificate")}
          >
            CERTIFICATE
          </Button>
        </div>
      </div>

      {/* Render the selected template */}
      <div className="animate-in fade-in zoom-in-95 duration-300">
        {isInvoice ? (
          <DebitNoteTemplate
            riskNote={riskNote}
            client={client}
            policy={policy}
          />
        ) : (
          <CertificateTemplate
            riskNote={riskNote}
            client={client}
            policy={policy}
          />
        )}
      </div>
    </div>
  )
}
