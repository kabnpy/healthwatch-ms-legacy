import { zodResolver } from "@hookform/resolvers/zod"
import { FileIcon, Plus } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"
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
import { getDocumentColumns } from "./DocumentColumns"

interface DocumentManagerProps {
  ownerId: string
  ownerType: "client" | "policy"
  title?: string
}

const documentSchema = z.object({
  subject: z.string().min(1, "Name is required"),
  summary: z.string().optional(),
  file_path: z.string().min(1, "URL or path is required"),
})

type DocumentFormData = z.infer<typeof documentSchema>

export function DocumentManager({
  ownerId,
  ownerType,
  title = "Documents",
}: DocumentManagerProps) {
  const { data: correspondences, isLoading } = useCorrespondences(ownerId)
  const [isUploadOpen, setIsOpen] = useState(false)
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const createCorrespondence = useCreateCorrespondence()

  const columns = getDocumentColumns()

  const form = useForm<DocumentFormData>({
    resolver: zodResolver(documentSchema),
    defaultValues: {
      subject: "",
      summary: "",
      file_path: "",
    },
  })

  const onSubmit = (data: DocumentFormData) => {
    // For now, we use the client correspondence endpoint regardless
    // Future: Use specific policy endpoint if ownerType is policy
    createCorrespondence.mutate(
      {
        clientId: ownerId,
        data: {
          ...data,
          client_id: ownerId,
          date_logged: new Date().toISOString(),
        },
      },
      {
        onSuccess: () => {
          showSuccessToast("Document uploaded successfully")
          form.reset()
          setIsOpen(false)
        },
        onError: () => {
          showErrorToast("Failed to upload document")
        },
      },
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-tight text-primary">
          {title}
        </h2>
        <Dialog open={isUploadOpen} onOpenChange={setIsOpen}>
          <DialogTrigger asChild>
            <Button size="sm" className="gap-2">
              <Plus className="size-4" />
              Upload
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Upload Document</DialogTitle>
              <DialogDescription>
                Add a new file reference to this {ownerType}.
              </DialogDescription>
            </DialogHeader>
            <Form {...form}>
              <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="space-y-4"
              >
                <FormField
                  control={form.control}
                  name="subject"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Document Name</FormLabel>
                      <FormControl>
                        <Input placeholder="e.g. Identity Card" {...field} />
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
                      <FormLabel>Notes</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Optional notes about this file"
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
                          placeholder="https://example.com/file.pdf"
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
      </div>

      {isLoading ? (
        <div className="py-10 text-center text-muted-foreground animate-pulse">
          Fetching documents...
        </div>
      ) : !correspondences?.data || correspondences.data.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-12 border-2 border-dashed rounded-lg bg-muted/5">
          <div className="rounded-full bg-muted p-4 mb-4">
            <FileIcon className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold">Empty Folder</h3>
          <p className="text-muted-foreground max-w-xs mx-auto">
            No files have been uploaded for this {ownerType} yet.
          </p>
        </div>
      ) : (
        <DataTable
          columns={columns}
          data={correspondences.data}
          searchPlaceholder="Filter documents..."
        />
      )}
    </div>
  )
}
