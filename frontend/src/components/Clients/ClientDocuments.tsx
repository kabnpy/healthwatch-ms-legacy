import { zodResolver } from "@hookform/resolvers/zod"
import type { ColumnDef } from "@tanstack/react-table"
import { ExternalLink, FileText, Plus } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"
import type { CorrespondencePublic } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import useCustomToast from "@/hooks/useCustomToast"
import {
  useCorrespondences,
  useCreateCorrespondence,
} from "@/hooks/useInsurance"

interface ClientDocumentsProps {
  clientId: string
}

export function ClientDocuments({ clientId }: ClientDocumentsProps) {
  const { data: correspondences, isLoading } = useCorrespondences(clientId)

  const columns: ColumnDef<CorrespondencePublic>[] = [
    {
      accessorKey: "subject",
      header: "Subject",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <FileText className="size-4 text-muted-foreground" />
          <span className="font-medium">{row.original.subject}</span>
        </div>
      ),
    },
    {
      accessorKey: "summary",
      header: "Summary",
    },
    {
      accessorKey: "date_logged",
      header: "Date Logged",
      cell: ({ row }) =>
        row.original.date_logged
          ? new Date(row.original.date_logged).toLocaleDateString()
          : "N/A",
    },
    {
      id: "actions",
      cell: ({ row }) => (
        <div className="flex justify-end">
          <Button variant="ghost" size="sm" asChild>
            <a href={row.original.file_path} target="_blank" rel="noreferrer">
              <ExternalLink className="size-4 mr-2" />
              Open
            </a>
          </Button>
        </div>
      ),
    },
  ]

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-tight">Client Documents</h2>
        <AddCorrespondence clientId={clientId} />
      </div>

      {isLoading ? (
        <div className="py-10 text-center">Loading documents...</div>
      ) : !correspondences?.data || correspondences.data.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-12 border-2 border-dashed rounded-lg bg-muted/5">
          <div className="rounded-full bg-muted p-4 mb-4">
            <FileText className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold">No documents found</h3>
          <p className="text-muted-foreground">
            Upload IDs, KRA PIN certificates, or letters here.
          </p>
        </div>
      ) : (
        <DataTable columns={columns} data={correspondences.data} />
      )}
    </div>
  )
}

const correspondenceSchema = z.object({
  subject: z.string().min(1, "Subject is required"),
  summary: z.string().optional(),
  file_path: z.string().min(1, "File path is required"), // For MVP, we just take a URL/Path string
})

type CorrespondenceFormData = z.infer<typeof correspondenceSchema>

function AddCorrespondence({ clientId }: { clientId: string }) {
  const [isOpen, setIsOpen] = useState(false)
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const createCorrespondence = useCreateCorrespondence()

  const form = useForm<CorrespondenceFormData>({
    resolver: zodResolver(correspondenceSchema),
    defaultValues: {
      subject: "",
      summary: "",
      file_path: "",
    },
  })

  const onSubmit = (data: CorrespondenceFormData) => {
    createCorrespondence.mutate(
      {
        clientId,
        data: {
          ...data,
          client_id: clientId,
          date_logged: new Date().toISOString(),
        },
      },
      {
        onSuccess: () => {
          showSuccessToast("Document added successfully")
          form.reset()
          setIsOpen(false)
        },
        onError: () => {
          showErrorToast("Failed to add document")
        },
      },
    )
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button size="sm" className="gap-2">
          <Plus className="size-4" />
          Upload Document
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add Client Document</DialogTitle>
          <DialogDescription>
            Attach a document reference to this client's file.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="subject"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Document Subject</FormLabel>
                  <FormControl>
                    <Input placeholder="e.g. KRA PIN Certificate" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="summary"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Summary / Notes</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Brief description of the document"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="file_path"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>File Path / URL</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="https://storage.example.com/file.pdf"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <div className="flex justify-end gap-2 pt-4">
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsOpen(false)}
              >
                Cancel
              </Button>
              <LoadingButton
                type="submit"
                loading={createCorrespondence.isPending}
              >
                Save Document
              </LoadingButton>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}
