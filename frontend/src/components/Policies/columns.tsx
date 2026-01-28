import { Link } from "@tanstack/react-router"
import type { ColumnDef } from "@tanstack/react-table"
import {
  Copy,
  ExternalLink,
  MoreHorizontal,
  ReceiptText,
  ShieldCheck,
} from "lucide-react"
import { toast } from "sonner"

import type { PolicyPublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

export const columns: ColumnDef<PolicyPublic>[] = [
  {
    accessorKey: "policy_number",
    header: "Policy Number",
    cell: ({ row }) => (
      <Link
        to="/policies/$policyId"
        params={{ policyId: row.original.id }}
        className="font-medium hover:underline text-primary flex items-center gap-2"
      >
        {row.original.policy_number}
        <ExternalLink className="size-3 opacity-50" />
      </Link>
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
    cell: ({ row }) => {
      const policy = row.original

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Policy Actions</DropdownMenuLabel>
            <DropdownMenuItem
              onClick={() => {
                navigator.clipboard.writeText(policy.id)
                toast.success("Policy ID copied to clipboard")
              }}
            >
              <Copy className="mr-2 h-4 w-4" />
              Copy ID
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <Link to="/policies/$policyId" params={{ policyId: policy.id }}>
                <ExternalLink className="mr-2 h-4 w-4" />
                View Dashboard
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link
                to="/policies/$policyId"
                params={{ policyId: policy.id }}
                hash="risk-notes"
              >
                <ReceiptText className="mr-2 h-4 w-4" />
                Risk Notes
              </Link>
            </DropdownMenuItem>
            <DropdownMenuItem asChild>
              <Link
                to="/policies/$policyId"
                params={{ policyId: policy.id }}
                hash="certificates"
              >
                <ShieldCheck className="mr-2 h-4 w-4" />
                Certificates
              </Link>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]
