import { Printer, X } from "lucide-react"
import { type ReactNode, useRef } from "react"
import { useReactToPrint } from "react-to-print"

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"

interface DocumentViewerModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: ReactNode
}

export function DocumentViewerModal({
  isOpen,
  onClose,
  title,
  children,
}: DocumentViewerModalProps) {
  const printRef = useRef<HTMLDivElement>(null)

  const handlePrint = useReactToPrint({
    contentRef: printRef,
    documentTitle: title,
  })

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-[900px] h-[90vh] flex flex-col p-0 gap-0">
        <DialogHeader className="px-6 py-4 border-b flex flex-row items-center justify-between space-y-0">
          <DialogTitle>{title}</DialogTitle>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => handlePrint()}
              className="gap-2"
            >
              <Printer className="size-4" />
              Print
            </Button>
            <DialogClose asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8">
                <X className="size-4" />
                <span className="sr-only">Close</span>
              </Button>
            </DialogClose>
          </div>
        </DialogHeader>

        <div className="flex-1 overflow-auto bg-gray-100 p-8 flex justify-center">
          {/* The Document Container - A4-ish proportions */}
          <div
            ref={printRef}
            className="bg-white shadow-lg w-[210mm] min-h-[297mm] relative print:w-full print:h-full print:shadow-none"
          >
            {children}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}
