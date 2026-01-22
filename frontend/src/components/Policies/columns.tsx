import type { ColumnDef } from "@tanstack/react-table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Link } from "@tanstack/react-router"
import type { PolicyPublic } from "@/client"
import { AddRiskNote } from "@/components/Insurance/AddRiskNote"
import { Eye } from "lucide-react"

export const columns: ColumnDef<PolicyPublic>[] = [
  {
    accessorKey: "policy_number",
    header: "Policy Number",
    cell: ({ row }) => (
      <span className="font-medium">{row.original.policy_number}</span>
    ),
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.original.status
      return (
        <Badge variant={status === "Active" ? "default" : "secondary"}>
          {status}
        </Badge>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end gap-2">
        <Button variant="ghost" size="sm" asChild>
          <Link to="/policies/$policyId" params={{ policyId: row.original.id }}>
            <Eye className="size-4 mr-2" />
            View
          </Link>
        </Button>
        <AddRiskNote 
          policyId={row.original.id} 
          policyNumber={row.original.policy_number} 
        />
      </div>
    ),
  },
]