import { FilePlus } from "lucide-react"
import { useState } from "react"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { RiskNoteForm } from "./RiskNoteForm"

interface AddRiskNoteProps {
  policyId: string
  policyNumber: string
}

export const AddRiskNote = ({ policyId, policyNumber }: AddRiskNoteProps) => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <Button size="sm" variant="outline" className="gap-2">
          <FilePlus className="size-4" />
          Add Risk Note
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>New Risk Note</DialogTitle>
          <DialogDescription>
            Creating risk note for policy <strong>{policyNumber}</strong>
          </DialogDescription>
        </DialogHeader>
        <RiskNoteForm
          policyId={policyId}
          onSuccess={() => setIsOpen(false)}
          onCancel={() => setIsOpen(false)}
        />
      </DialogContent>
    </Dialog>
  )
}
