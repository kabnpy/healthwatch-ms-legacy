import { useSuspenseQuery } from "@tanstack/react-query"
import { ClientsService, FinancialsService, PoliciesService, RiskNotesService } from "@/client"
import type { RiskNotePublic, InvoicePublic, ClientPublic, PolicyPublic, ReceiptPublic } from "@/client"
import { RiskNoteTemplate } from "./templates/RiskNoteTemplate"
import { InvoiceTemplate } from "./templates/InvoiceTemplate"
import { ReceiptTemplate } from "./templates/ReceiptTemplate"

// --- Query Options ---

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
  }
}

function getClientQueryOptions(clientId: string) {
  return {
    queryFn: () => ClientsService.readClient({ id: clientId }),
    queryKey: ["clients", clientId],
  }
}

// --- Loader Components ---

function RiskNoteLoader({ id }: { id: string }) {
  const { data: riskNote } = useSuspenseQuery(getRiskNoteQueryOptions(id)) as { data: RiskNotePublic }
  const { data: policy } = useSuspenseQuery(getPolicyQueryOptions(riskNote.policy_id)) as { data: PolicyPublic }
  const { data: client } = useSuspenseQuery(getClientQueryOptions(policy.client_id)) as { data: ClientPublic }

  return <RiskNoteTemplate riskNote={riskNote} client={client} policy={policy} />
}

function InvoiceLoader({ id }: { id: string }) {

  const { data: invoice } = useSuspenseQuery(getInvoiceQueryOptions(id)) as { data: InvoicePublic }

  const { data: client } = useSuspenseQuery(getClientQueryOptions(invoice.client_id)) as { data: ClientPublic }



  return (

    <InvoiceTemplate 

      invoice={invoice} 

      client={client} 

      lineItems={(invoice as any).line_items || []} 

    />

  )

}



function ReceiptLoader({ id }: { id: string }) {

  const { data: receipt } = useSuspenseQuery({

    queryFn: () => FinancialsService.readReceiptById({ id }),

    queryKey: ["receipts", id],

  }) as { data: ReceiptPublic }

  const { data: client } = useSuspenseQuery(getClientQueryOptions(receipt.client_id)) as { data: ClientPublic }



  return <ReceiptTemplate receipt={receipt} client={client} />

}



// --- Main Component ---



type DocumentType = "risknote" | "invoice" | "receipt"



interface UniversalDocumentViewerProps {

  id: string

  type: DocumentType

}



export function UniversalDocumentViewer({

  id,

  type,

}: UniversalDocumentViewerProps) {

  return (

    <div className="w-full h-full animate-in fade-in zoom-in-95 duration-300">

      {type === "risknote" && <RiskNoteLoader id={id} />}

      

      {type === "invoice" && <InvoiceLoader id={id} />}



      {type === "receipt" && <ReceiptLoader id={id} />}

    </div>

  )

}
