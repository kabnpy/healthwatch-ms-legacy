import { useSuspenseQuery } from "@tanstack/react-query"
import { Suspense, useMemo, useState } from "react"
import { FinancialsService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import { UniversalDocumentViewer } from "@/components/Documents/UniversalDocumentViewer"
import { getColumns as getInvoiceColumns } from "@/components/Invoices/columns"
import PendingItems from "@/components/Pending/PendingItems"

function getInvoicesQueryOptions(clientId: string) {
  return {
    queryFn: () =>
      FinancialsService.readInvoices({ clientId, skip: 0, limit: 100 }),
    queryKey: ["invoices", { clientId }],
  }
}

interface ClientInvoicesProps {
  clientId: string
}

export function ClientInvoices({ clientId }: ClientInvoicesProps) {
  const { data: invoices } = useSuspenseQuery(getInvoicesQueryOptions(clientId))

  const [viewerOpen, setViewerOpen] = useState(false)
  const [selectedInvoiceId, setSelectedInvoiceId] = useState<string | null>(
    null,
  )

  const invoiceColumns = useMemo(
    () =>
      getInvoiceColumns((invoice) => {
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

      {!invoices?.data || invoices.data.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-12 border rounded-lg bg-muted/5">
          <h3 className="text-lg font-semibold">No invoices issued</h3>
          <p className="text-muted-foreground">
            Invoices will appear here once policies are issued or renewed.
          </p>
        </div>
      ) : (
        <DataTable
          columns={invoiceColumns}
          data={invoices.data}
          searchPlaceholder="Search invoices..."
        />
      )}

      {selectedInvoiceId && (
        <DocumentViewerModal
          isOpen={viewerOpen}
          onClose={() => setViewerOpen(false)}
          title={`Invoice Details`}
        >
          <Suspense fallback={<PendingItems />}>
            <UniversalDocumentViewer id={selectedInvoiceId} type="invoice" />
          </Suspense>
        </DocumentViewerModal>
      )}
    </div>
  )
}
