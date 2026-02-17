import type { ColumnDef } from "@tanstack/react-table"
import { useState } from "react"
import { toast } from "sonner"
import type { InvoicePublic, ReceiptPublic } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { useAllocateReceipt, useInvoices } from "@/hooks/useFinancials"

interface AllocationDialogProps {
  receipt: ReceiptPublic
  isOpen: boolean
  onClose: () => void
}

export function AllocationDialog({
  receipt,
  isOpen,
  onClose,
}: AllocationDialogProps) {
  const { data: invoicesData, isLoading } = useInvoices(receipt.client_id)
  const allocateMutation = useAllocateReceipt()
  const [allocationAmounts, setAllocationAmounts] = useState<
    Record<string, number>
  >({})

  const unallocated = Number(
    (receipt as any).unallocated_amount ?? receipt.amount,
  )

  // Filter only unpaid or partial invoices
  const pendingInvoices =
    invoicesData?.data.filter((inv) => Number(inv.balance_due || 0) > 0) || []

  const handleAllocate = async (invoiceId: string) => {
    const amount = allocationAmounts[invoiceId]
    if (!amount || amount <= 0) {
      toast.error("Please enter a valid amount")
      return
    }

    if (amount > unallocated) {
      toast.error(
        `Cannot allocate more than available balance (KES ${unallocated.toLocaleString()})`,
      )
      return
    }

    try {
      await allocateMutation.mutateAsync({
        id: receipt.id,
        data: {
          receipt_id: receipt.id,
          invoice_id: invoiceId,
          amount_allocated: amount,
        },
      })
      toast.success("Amount allocated successfully")
      setAllocationAmounts((prev) => ({ ...prev, [invoiceId]: 0 }))
    } catch (_error) {
      toast.error("Allocation failed")
    }
  }

  const columns: ColumnDef<InvoicePublic>[] = [
    {
      accessorKey: "invoice_number",
      header: "Invoice #",
    },
    {
      accessorKey: "balance_due",
      header: "Balance Due",
      cell: ({ row }) => (
        <span className="font-mono text-destructive">
          KES {Number(row.original.balance_due || 0).toLocaleString()}
        </span>
      ),
    },
    {
      id: "action",
      header: "Allocate",
      cell: ({ row }) => (
        <div className="flex gap-2">
          <Input
            type="number"
            className="w-24 h-8"
            placeholder="Amount"
            value={allocationAmounts[row.original.id] || ""}
            max={Math.min(unallocated, Number(row.original.balance_due || 0))}
            onChange={(e) =>
              setAllocationAmounts((prev) => ({
                ...prev,
                [row.original.id]: parseFloat(e.target.value),
              }))
            }
          />
          <Button
            size="sm"
            className="h-8"
            onClick={() => handleAllocate(row.original.id)}
            disabled={allocateMutation.isPending || unallocated <= 0}
          >
            Apply
          </Button>
        </div>
      ),
    },
  ]

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Allocate Receipt {receipt.receipt_number}</DialogTitle>
          <DialogDescription className="flex justify-between items-center pt-2">
            <span>
              Receipt Total:{" "}
              <span className="font-bold text-foreground">
                KES {Number(receipt.amount).toLocaleString()}
              </span>
            </span>
            <span
              className={
                unallocated > 0
                  ? "text-green-600 font-bold"
                  : "text-muted-foreground"
              }
            >
              Available: KES {unallocated.toLocaleString()}
            </span>
          </DialogDescription>
        </DialogHeader>

        <div className="py-4">
          <h4 className="text-sm font-medium mb-4">Pending Invoices</h4>
          {isLoading ? (
            <p>Loading invoices...</p>
          ) : (
            <DataTable columns={columns} data={pendingInvoices} />
          )}
        </div>

        <div className="flex justify-end gap-2">
          <Button variant="outline" onClick={onClose}>
            Done
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
