import { useSuspenseQuery } from "@tanstack/react-query"
import { Suspense, useMemo, useState } from "react"
import { PoliciesService, RiskNotesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import { UniversalDocumentViewer } from "@/components/Documents/UniversalDocumentViewer"
import PendingItems from "@/components/Pending/PendingItems"
import { getColumns as getRiskNoteColumns } from "@/components/RiskNotes/columns"

function getPoliciesQueryOptions(clientId: string) {
  return {
    queryFn: () =>
      PoliciesService.readPolicies({ clientId, skip: 0, limit: 100 }),
    queryKey: ["policies", { clientId }],
  }
}

function getClientRiskNotesQueryOptions() {
  return {
    queryFn: () => RiskNotesService.readRiskNotes({ skip: 0, limit: 1000 }),
    queryKey: ["risk-notes"],
  }
}

interface ClientInvoicesProps {
  clientId: string
}

export function ClientInvoices({ clientId }: ClientInvoicesProps) {
  const { data: policies } = useSuspenseQuery(getPoliciesQueryOptions(clientId))
  const { data: allRiskNotes } = useSuspenseQuery(
    getClientRiskNotesQueryOptions(),
  )

  const [viewerOpen, setViewerOpen] = useState(false)
  const [selectedInvoiceId, setSelectedInvoiceId] = useState<string | null>(
    null,
  )

  const policyIds = new Set(policies.data.map((p) => p.id))
  const clientInvoices = allRiskNotes.data.filter((rn) =>
    policyIds.has(rn.policy_id),
  )

  const invoiceColumns = useMemo(
    () =>
      getRiskNoteColumns((invoice) => {
        setSelectedInvoiceId(invoice.id)
        setViewerOpen(true)
      }),
    [],
  )

  return (
    <div className="space-y-4 pt-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-tight text-primary">
          Financial Statement / Invoices
        </h2>
      </div>

      {clientInvoices.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-12 border rounded-lg bg-muted/5">
          <h3 className="text-lg font-semibold">No invoices issued</h3>
          <p className="text-muted-foreground">
            Invoices will appear here once policies are issued or renewed.
          </p>
        </div>
      ) : (
        <DataTable columns={invoiceColumns} data={clientInvoices} />
      )}

      {selectedInvoiceId && (
        <DocumentViewerModal
          isOpen={viewerOpen}
          onClose={() => setViewerOpen(false)}
          title={`Invoice: ${selectedInvoiceId}`}
        >
          <Suspense fallback={<PendingItems />}>
            <UniversalDocumentViewer id={selectedInvoiceId} type="invoice" />
          </Suspense>
        </DocumentViewerModal>
      )}
    </div>
  )
}
