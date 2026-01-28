import type { ColumnDef } from "@tanstack/react-table"
import { Copy, Eye, FileDown, Mail, MoreHorizontal } from "lucide-react"
import { toast } from "sonner"

import type { RiskNotePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export const getColumns = (
  onView: (riskNote: RiskNotePublic) => void,
): ColumnDef<RiskNotePublic>[] => [
  {
    accessorKey: "risk_note_number",
    header: "Risk Note #",
    cell: ({ row }) => (
      <button
        type="button"
        onClick={() => onView(row.original)}
        className="font-mono font-medium text-primary hover:underline"
      >
        {row.original.risk_note_number}
      </button>
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
          {breakdown?.total?.toLocaleString(undefined, {
            minimumFractionDigits: 2,
          }) || "0.00"}
        </span>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => {
      const riskNote = row.original

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Actions</DropdownMenuLabel>
            <DropdownMenuItem
              onClick={() => {
                navigator.clipboard.writeText(riskNote.id)
                toast.success("ID copied to clipboard")
              }}
            >
              <Copy className="mr-2 h-4 w-4" />
              Copy ID
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => onView(riskNote)}>
              <Eye className="mr-2 h-4 w-4" />
              View Document
            </DropdownMenuItem>
            <DropdownMenuItem disabled>
              <FileDown className="mr-2 h-4 w-4" />
              Download PDF
            </DropdownMenuItem>
            <DropdownMenuItem disabled>
              <Mail className="mr-2 h-4 w-4" />
              Email to Client
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]
