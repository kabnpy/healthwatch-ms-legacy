import { Link } from "@tanstack/react-router"
import type { ColumnDef } from "@tanstack/react-table"
import { ExternalLink } from "lucide-react"

import type { ClientPublic } from "@/client"

export const columns: ColumnDef<ClientPublic>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => (
      <Link
        to="/clients/$clientId"
        params={{ clientId: row.original.id }}
        className="font-medium hover:underline flex items-center gap-2"
      >
        {row.original.name}
        <ExternalLink className="size-3 text-muted-foreground" />
      </Link>
    ),
  },
  {
    accessorKey: "kra_pin",
    header: "KRA PIN",
  },
  {
    accessorKey: "email",
    header: "Email",
    cell: ({ row }) => row.original.email || "N/A",
  },
  {
    accessorKey: "phone",
    header: "Phone",
  },
  {
    accessorKey: "client_type",
    header: "Type",
  },
]
