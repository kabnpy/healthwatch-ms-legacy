import type { ColumnDef } from "@tanstack/react-table"
import {
  Copy,
  ExternalLink,
  FileIcon,
  FileImage,
  FileText,
  MoreHorizontal,
  Trash2,
} from "lucide-react"
import { toast } from "sonner"
import type { CorrespondencePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

const getFileIcon = (filePath: string) => {
  const ext = filePath.split(".").pop()?.toLowerCase()
  if (["jpg", "jpeg", "png", "webp"].includes(ext || "")) return FileImage
  if (["pdf"].includes(ext || "")) return FileText
  return FileIcon
}

export const getDocumentColumns = (): ColumnDef<CorrespondencePublic>[] => [
  {
    accessorKey: "subject",
    header: "Document Name",
    cell: ({ row }) => {
      const Icon = getFileIcon(row.original.file_path)
      return (
        <div className="flex items-center gap-3">
          <div className="p-2 bg-muted rounded-md">
            <Icon className="size-4 text-muted-foreground" />
          </div>
          <div className="flex flex-col">
            <span className="font-medium text-sm">{row.original.subject}</span>
            <span className="text-[10px] text-muted-foreground uppercase tracking-tight">
              {row.original.file_path.split(".").pop() || "FILE"}
            </span>
          </div>
        </div>
      )
    },
  },
  {
    accessorKey: "summary",
    header: "Description / Notes",
    cell: ({ row }) => (
      <span className="text-sm text-muted-foreground">
        {row.original.summary || "—"}
      </span>
    ),
  },
  {
    accessorKey: "date_logged",
    header: "Logged Date",
    cell: ({ row }) => (
      <span className="text-sm">
        {row.original.date_logged
          ? new Date(row.original.date_logged).toLocaleDateString(undefined, {
              dateStyle: "medium",
            })
          : "N/A"}
      </span>
    ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => {
      const doc = row.original

      return (
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" className="h-8 w-8 p-0">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>Document Actions</DropdownMenuLabel>
            <DropdownMenuItem
              onClick={() => {
                navigator.clipboard.writeText(doc.file_path)
                toast.success("Link copied to clipboard")
              }}
            >
              <Copy className="mr-2 h-4 w-4" />
              Copy Link
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem asChild>
              <a href={doc.file_path} target="_blank" rel="noreferrer">
                <ExternalLink className="mr-2 h-4 w-4" />
                View Document
              </a>
            </DropdownMenuItem>
            <DropdownMenuItem
              className="text-destructive focus:bg-destructive/10 focus:text-destructive"
              disabled
            >
              <Trash2 className="mr-2 h-4 w-4" />
              Delete Permanently
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      )
    },
  },
]
