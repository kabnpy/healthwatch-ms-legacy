import { useSuspenseQuery } from "@tanstack/react-query"
import type {
  ClientPublic,
  InvoicePublic,
  PolicyPublic,
  RiskNotePublic,
} from "@/client"
import {
  ClientsService,
  FinancialsService,
  PoliciesService,
  RiskNotesService,
} from "@/client"
import { InvoiceTemplate } from "./templates/InvoiceTemplate"
import { RiskNoteTemplate } from "./templates/RiskNoteTemplate"

function getRiskNoteQueryOptions(id: string) {
  return {
    queryFn: () => RiskNotesService.readRiskNote({ id }),
    queryKey: ["risk-notes", id],
  }
}

function getInvoiceQueryOptions(id: string) {
  return {
    queryFn: () => FinancialsService.readInvoice({ id }),
    queryKey: ["invoices", id],
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

export function UniversalDocumentViewer({
  id,
  type,
}: UniversalDocumentViewerProps) {
  const isInvoice = type === "invoice"

  // 1. Fetch main document
  const { data: riskNote } = useSuspenseQuery({
    ...getRiskNoteQueryOptions(id),
    enabled: !isInvoice && type !== "receipt",
  } as any) as { data: RiskNotePublic }

  const { data: invoice } = useSuspenseQuery({
    ...getInvoiceQueryOptions(id),
    enabled: isInvoice,
  } as any) as { data: InvoicePublic }

  // 2. Fetch dependencies
  const { data: policy } = useSuspenseQuery({
    ...getPolicyQueryOptions(riskNote?.policy_id),
    enabled: !!riskNote?.policy_id,
  } as any) as { data: PolicyPublic }

  const clientId = isInvoice ? invoice?.client_id : policy?.client_id

  const { data: client } = useSuspenseQuery({
    ...getClientQueryOptions(clientId),
    enabled: !!clientId,
  } as any) as { data: ClientPublic }

  return (
    <div className="w-full h-full animate-in fade-in zoom-in-95 duration-300">
      {type === "risknote" && riskNote && client && policy && (
        <RiskNoteTemplate riskNote={riskNote} client={client} policy={policy} />
      )}

      {isInvoice && invoice && client && (
        <InvoiceTemplate
          invoice={invoice}
          client={client}
          lineItems={(invoice as any).line_items || []}
        />
      )}

      {type === "receipt" && (
        <div className="p-8 text-center text-muted-foreground italic border rounded-lg">
          Receipt View Placeholder - Coming Soon
        </div>
      )}
    </div>
  )
}
