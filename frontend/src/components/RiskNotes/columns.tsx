import type { ColumnDef } from "@tanstack/react-table"
import { Printer } from "lucide-react"
import { Link } from "@tanstack/react-router"

import type { RiskNotePublic } from "@/client"
import { Button } from "@/components/ui/button"

export const columns: ColumnDef<RiskNotePublic>[] = [
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
    cell: ({ row }) => (
      <span className="font-bold">
        {row.original.gross_premium.toLocaleString(undefined, { minimumFractionDigits: 2 })}
      </span>
    ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <Button size="sm" variant="ghost" asChild>
          <Link
            to="/print/risk-notes/$id"
            params={{ id: row.original.id }}
            target="_blank"
          >
            <Printer className="size-4 mr-2" />
            Print
          </Link>
        </Button>
      </div>
    ),
  },
]