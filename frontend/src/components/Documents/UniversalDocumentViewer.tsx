import { useSuspenseQuery } from "@tanstack/react-query"
import { ClientsService, PoliciesService, RiskNotesService } from "@/client"
import { DebitNoteTemplate } from "./templates/DebitNoteTemplate"
import { RiskNoteTemplate } from "./templates/RiskNoteTemplate"

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

type DocumentType = "risknote" | "invoice" | "receipt"

interface UniversalDocumentViewerProps {
  id: string
  type: DocumentType
}

/**
 * Universal Document Viewer
 * A generic container that fetches required data and renders the appropriate template.
 * Displays only the document requested (no internal toggles).
 */
export function UniversalDocumentViewer({
  id,
  type,
}: UniversalDocumentViewerProps) {
  const { data: riskNote } = useSuspenseQuery(getRiskNoteQueryOptions(id))
  const { data: policy } = useSuspenseQuery(
    getPolicyQueryOptions(riskNote.policy_id),
  )
  const { data: client } = useSuspenseQuery(
    getClientQueryOptions(policy.client_id),
  )

  return (
    <div className="w-full h-full animate-in fade-in zoom-in-95 duration-300">
      {type === "risknote" && (
        <RiskNoteTemplate riskNote={riskNote} client={client} policy={policy} />
      )}
      {type === "invoice" && (
        <DebitNoteTemplate
          riskNote={riskNote}
          client={client}
          policy={policy}
        />
      )}
      {/* Receipt template coming in Phase 3 */}
      {type === "receipt" && (
        <div className="p-8 text-center text-muted-foreground italic border rounded-lg">
          Receipt View Placeholder - Coming Soon
        </div>
      )}
    </div>
  )
}
