import { Suspense, useMemo, useState } from "react"
import { DataTable } from "@/components/Common/DataTable"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import { UniversalDocumentViewer } from "@/components/Documents/UniversalDocumentViewer"
import { getColumns as getInvoiceColumns } from "@/components/Invoices/columns"
import { getReceiptColumns } from "@/components/Financials/ReceiptColumns"
import PendingItems from "@/components/Pending/PendingItems"
import { useFinancialSummary } from "@/hooks/useFinancials"
import { SummaryCard } from "@/components/Common/SummaryCard"
import { Wallet, Receipt as ReceiptIcon, CreditCard, Plus } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { AddReceiptForm } from "@/components/Financials/AddReceiptForm"
import { AllocationDialog } from "@/components/Financials/AllocationDialog"
import type { ReceiptPublic } from "@/client"

interface ClientInvoicesProps {
  clientId: string
}

export function ClientInvoices({ clientId }: ClientInvoicesProps) {
  const { invoices, receipts, summary, isLoading } = useFinancialSummary(clientId)

  const [viewerOpen, setViewerOpen] = useState(false)
  const [selectedInvoiceId, setSelectedInvoiceId] = useState<string | null>(null)
  
  const [isAddReceiptOpen, setIsAddReceiptOpen] = useState(false)
  const [selectedReceipt, setSelectedReceipt] = useState<ReceiptPublic | null>(null)
  const [isAllocationOpen, setIsAllocationOpen] = useState(false)

  const handleAllocate = (receipt: ReceiptPublic) => {
    setSelectedReceipt(receipt)
    setIsAllocationOpen(true)
  }

  const invoiceColumns = useMemo(
    () =>
      getInvoiceColumns((invoice) => {
        setSelectedInvoiceId(invoice.id)
        setViewerOpen(true)
      }),
    [],
  )

  const receiptColumns = useMemo(() => getReceiptColumns(handleAllocate), [])

  if (isLoading) return <PendingItems />

  return (
    <div className="space-y-6 pt-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight text-primary">
          Financial Statement
        </h2>
        <Button className="gap-2" onClick={() => setIsAddReceiptOpen(true)}>
          <Plus className="size-4" />
          Log Payment
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <SummaryCard
          title="Total Invoiced"
          value={`KES ${summary.totalInvoiced.toLocaleString()}`}
          description="Billed for all policies"
          icon={ReceiptIcon}
        />
        <SummaryCard
          title="Total Paid"
          value={`KES ${summary.totalPaid.toLocaleString()}`}
          description="Verified receipts"
          icon={Wallet}
        />
        <SummaryCard
          title="Outstanding Balance"
          value={`KES ${summary.totalDue.toLocaleString()}`}
          description="Current due amount"
          icon={CreditCard}
        />
      </div>

      <Tabs defaultValue="invoices" className="w-full">
        <TabsList>
          <TabsTrigger value="invoices">Invoices</TabsTrigger>
          <TabsTrigger value="receipts">Receipts / Payments</TabsTrigger>
        </TabsList>

        <TabsContent value="invoices" className="pt-4">
          <DataTable
            columns={invoiceColumns}
            data={invoices}
            searchPlaceholder="Search invoices..."
          />
        </TabsContent>

        <TabsContent value="receipts" className="pt-4">
          <DataTable
            columns={receiptColumns}
            data={receipts}
            searchPlaceholder="Search receipts..."
          />
        </TabsContent>
      </Tabs>

      {/* MODALS */}
      <Dialog open={isAddReceiptOpen} onOpenChange={setIsAddReceiptOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Log Payment for Client</DialogTitle>
            <DialogDescription>
              Record a new receipt in the system.
            </DialogDescription>
          </DialogHeader>
          <AddReceiptForm 
            initialClientId={clientId}
            onSuccess={() => setIsAddReceiptOpen(false)} 
            onCancel={() => setIsAddReceiptOpen(false)} 
          />
        </DialogContent>
      </Dialog>

      {selectedReceipt && (
        <AllocationDialog
          receipt={selectedReceipt}
          isOpen={isAllocationOpen}
          onClose={() => setIsAllocationOpen(false)}
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
