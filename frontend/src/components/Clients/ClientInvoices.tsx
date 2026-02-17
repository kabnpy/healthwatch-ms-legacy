import { FilePlus, FileText, Plus, Receipt } from "lucide-react"
import { Suspense, useCallback, useMemo, useState } from "react"
import type { InvoicePublic, ReceiptPublic } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import { EmptyState } from "@/components/Common/EmptyState"
import { DocumentViewer } from "@/components/Documents/DocumentViewer"
import { AddReceiptForm } from "@/components/Financials/AddReceiptForm"
import { AllocationDialog } from "@/components/Financials/AllocationDialog"
import { AllocationHistory } from "@/components/Financials/AllocationHistory"
import { InvoicesSkeleton } from "@/components/Financials/InvoicesSkeleton"
import { InvoiceWizard } from "@/components/Financials/InvoiceWizard"
import { getReceiptColumns } from "@/components/Financials/ReceiptColumns"
import { getColumns as getInvoiceColumns } from "@/components/Invoices/columns"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useFinancialSummary, useVoidReceipt } from "@/hooks/useFinancials"

interface ClientInvoicesProps {
  clientId: string
}

export function ClientInvoices({ clientId }: ClientInvoicesProps) {
  const { invoices, receipts, isLoading } = useFinancialSummary(clientId)
  const voidMutation = useVoidReceipt()

  const [viewerOpen, setViewerOpen] = useState(false)
  const [selectedDoc, setSelectedDoc] = useState<{
    id: string
    type: "invoice" | "receipt"
  } | null>(null)

  const [isAddReceiptOpen, setIsAddReceiptOpen] = useState(false)
  const [isInvoiceWizardOpen, setIsInvoiceWizardOpen] = useState(false)
  const [selectedReceipt, setSelectedReceipt] = useState<ReceiptPublic | null>(
    null,
  )
  const [isAllocationOpen, setIsAllocationOpen] = useState(false)
  const [receiptToVoid, setReceiptToVoid] = useState<ReceiptPublic | null>(null)

  const [historyTarget, setHistoryTarget] = useState<{
    type: "invoice" | "receipt"
    item: InvoicePublic | ReceiptPublic
  } | null>(null)

  const handleAllocate = useCallback((receipt: ReceiptPublic) => {
    setSelectedReceipt(receipt)
    setIsAllocationOpen(true)
  }, [])

  const handleVoid = async () => {
    if (!receiptToVoid) return
    try {
      await voidMutation.mutateAsync(receiptToVoid.id)
      setReceiptToVoid(null)
    } catch (_error) {
      // toast is already in mutation
    }
  }

  const invoiceColumns = useMemo(
    () =>
      getInvoiceColumns(
        (invoice) => {
          setSelectedDoc({ id: invoice.id, type: "invoice" })
          setViewerOpen(true)
        },
        (invoice) => setHistoryTarget({ type: "invoice", item: invoice }),
      ),
    [],
  )

  const receiptColumns = useMemo(
    () =>
      getReceiptColumns(
        handleAllocate,
        (receipt) => setHistoryTarget({ type: "receipt", item: receipt }),
        (receipt) => setReceiptToVoid(receipt),
        (receipt) => {
          setSelectedDoc({ id: receipt.id, type: "receipt" })
          setViewerOpen(true)
        },
      ),
    [handleAllocate],
  )

  if (isLoading) return <InvoicesSkeleton />

  return (
    <div className="space-y-6 pt-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight text-primary">
          Invoices
        </h2>
        <div className="flex gap-2">
          <Button
            variant="outline"
            className="gap-2"
            onClick={() => setIsInvoiceWizardOpen(true)}
          >
            <FilePlus className="size-4" />
            Generate Invoice
          </Button>
          <Button className="gap-2" onClick={() => setIsAddReceiptOpen(true)}>
            <Plus className="size-4" />
            Log Payment
          </Button>
        </div>
      </div>

      <Tabs defaultValue="invoices" className="w-full">
        <TabsList>
          <TabsTrigger value="invoices">Invoices</TabsTrigger>
          <TabsTrigger value="receipts">Receipts / Payments</TabsTrigger>
        </TabsList>

        <TabsContent value="invoices" className="pt-4">
          {invoices.length === 0 ? (
            <EmptyState
              title="No invoices found"
              description="There are no invoices for this client yet. Use the wizard to generate one from pending risk notes."
              icon={FileText}
              action={{
                label: "Generate Invoice",
                onClick: () => setIsInvoiceWizardOpen(true),
                icon: FilePlus,
              }}
            />
          ) : (
            <DataTable
              columns={invoiceColumns}
              data={invoices}
              searchPlaceholder="Search invoices..."
            />
          )}
        </TabsContent>

        <TabsContent value="receipts" className="pt-4">
          {receipts.length === 0 ? (
            <EmptyState
              title="No receipts found"
              description="No payments have been logged for this client yet."
              icon={Receipt}
              action={{
                label: "Log First Payment",
                onClick: () => setIsAddReceiptOpen(true),
                icon: Plus,
              }}
            />
          ) : (
            <DataTable
              columns={receiptColumns}
              data={receipts}
              searchPlaceholder="Search receipts..."
            />
          )}
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

      <InvoiceWizard
        clientId={clientId}
        isOpen={isInvoiceWizardOpen}
        onClose={() => setIsInvoiceWizardOpen(false)}
      />

      {selectedDoc && (
        <DocumentViewerModal
          isOpen={viewerOpen}
          onClose={() => {
            setViewerOpen(false)
            setSelectedDoc(null)
          }}
          title={`${selectedDoc.type === "invoice" ? "Invoice" : "Receipt"} Details`}
        >
          <Suspense fallback={<InvoicesSkeleton />}>
            <DocumentViewer id={selectedDoc.id} type={selectedDoc.type} />
          </Suspense>
        </DocumentViewerModal>
      )}

      {/* HISTORY DIALOG */}
      <Dialog
        open={!!historyTarget}
        onOpenChange={(open) => !open && setHistoryTarget(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {historyTarget?.type === "invoice"
                ? "Payment History"
                : "Allocation History"}
            </DialogTitle>
            <DialogDescription>
              {historyTarget?.type === "invoice"
                ? `Receipts applied to Invoice ${(historyTarget.item as InvoicePublic).invoice_number}`
                : `Invoices paid by Receipt ${(historyTarget?.item as ReceiptPublic)?.receipt_number}`}
            </DialogDescription>
          </DialogHeader>
          {historyTarget && (
            <AllocationHistory
              allocations={historyTarget.item.allocations || []}
              type={historyTarget.type}
            />
          )}
          <div className="flex justify-end pt-4">
            <Button variant="outline" onClick={() => setHistoryTarget(null)}>
              Close
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* VOID CONFIRMATION */}
      <Dialog
        open={!!receiptToVoid}
        onOpenChange={(open) => !open && setReceiptToVoid(null)}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="text-destructive">
              Void Receipt {receiptToVoid?.receipt_number}
            </DialogTitle>
            <DialogDescription>
              Are you sure you want to void this payment? This will:
              <ul className="list-disc pl-6 pt-2 space-y-1">
                <li>Reverse all allocations made from this receipt</li>
                <li>Increase the balance due on all affected invoices</li>
                <li>Mark this receipt as "Voided"</li>
              </ul>
              <p className="pt-2 font-semibold">
                This action cannot be undone.
              </p>
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setReceiptToVoid(null)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleVoid}
              disabled={voidMutation.isPending}
            >
              {voidMutation.isPending ? "Voiding..." : "Confirm Void"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}
