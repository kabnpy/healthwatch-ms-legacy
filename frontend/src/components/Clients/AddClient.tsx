import { Plus } from "lucide-react"
import { useState } from "react"

import type { ApiError, ClientCreate } from "@/client"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import useCustomToast from "@/hooks/useCustomToast"
import { useCreateClient } from "@/hooks/useInsurance"
import { handleError } from "@/utils"
import { ClientForm } from "./ClientForm"

export const AddClient = () => {
  const [isOpen, setIsOpen] = useState(false)
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const createClient = useCreateClient()

  const onSubmit = (data: ClientCreate) => {
    createClient.mutate(data, {
      onSuccess: () => {
        showSuccessToast("Client created successfully")
        setIsOpen(false)
      },
      onError: (err: Error) => {
        handleError.call(showErrorToast, err as ApiError)
      },
    })
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button className="gap-2">
          <Plus className="size-4" />
          Add Client
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>Add New Client</DialogTitle>
          <DialogDescription>
            Enter the details of the new client to add them to the system.
          </DialogDescription>
        </DialogHeader>
        <ClientForm
          onSubmit={onSubmit as any}
          onCancel={() => setIsOpen(false)}
          isLoading={createClient.isPending}
        />
      </DialogContent>
    </Dialog>
  )
}
