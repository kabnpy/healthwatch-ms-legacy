import type { ReceiptAllocationBase } from "@/client"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

interface AllocationHistoryProps {
  allocations: ReceiptAllocationBase[]
  type: "invoice" | "receipt"
}

export function AllocationHistory({ allocations, type }: AllocationHistoryProps) {
  if (allocations.length === 0) {
    return (
      <div className="text-center py-6 text-muted-foreground text-sm italic border rounded-md bg-muted/5">
        No allocations recorded yet.
      </div>
    )
  }

  return (
    <div className="border rounded-md">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>{type === "invoice" ? "Receipt ID" : "Invoice ID"}</TableHead>
            <TableHead className="text-right">Amount Allocated</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {allocations.map((allocation, index) => (
            <TableRow key={index}>
              <TableCell className="font-mono text-xs">
                {type === "invoice" ? allocation.receipt_id : allocation.invoice_id}
              </TableCell>
              <TableCell className="text-right font-bold">
                KES {allocation.amount_allocated.toLocaleString()}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
