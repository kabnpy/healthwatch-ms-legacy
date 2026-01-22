import type { ColumnDef } from "@tanstack/react-table"
import { Eye } from "lucide-react"

import type { RiskNotePublic } from "@/client"
import { Button } from "@/components/ui/button"

export const getColumns = (onView: (riskNote: RiskNotePublic) => void): ColumnDef<RiskNotePublic>[] => [
  {
    accessorKey: "risk_note_number",
    header: "Risk Note #",
    cell: ({ row }) => (
      <span className="font-mono">{row.original.risk_note_number}</span>
    ),
  },
  {
    accessorKey: "transaction_type",
    header: "Type",
  },
  {
    accessorKey: "start_date",
    header: "Start Date",
  },
  {
    accessorKey: "gross_premium",
    header: "Gross Premium",
    cell: ({ row }) => {
      const breakdown = row.original.premium_breakdown as any
      return (
        <span className="font-bold">
          {breakdown?.total?.toLocaleString(undefined, { minimumFractionDigits: 2 }) || "0.00"}
        </span>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <Button 
          size="sm" 
          variant="ghost" 
          onClick={() => onView(row.original)}
        >
          <Eye className="size-4 mr-2" />
          View
        </Button>
      </div>
    ),
  },
]