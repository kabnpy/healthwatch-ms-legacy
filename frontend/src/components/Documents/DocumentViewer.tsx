import { useQuery } from "@tanstack/react-query"
import { Download, FileText, Loader2, Printer } from "lucide-react"
import { Suspense } from "react"

import {
  DocumentsService,
  FinancialsService,
  type ReceiptPublic,
} from "@/client"
import { DocumentService, type DocumentSourceType } from "@/services/document"
import { InlineErrorFallback } from "../Common/ErrorFallbacks"
import { HTMLViewer } from "../Common/HTMLViewer"
import { Button } from "../ui/button"

// --- Types ---

type DocumentType = "risknote" | "invoice" | "receipt" | "external" | "renewal"

interface DocumentViewerProps {
  id: string
  type: DocumentType
}

// --- Shared Components ---

function DocumentShell({
  title,
  subtitle,
  children,
  headerExtra,
  footer,
}: {
  title: string
  subtitle?: string
  children: React.ReactNode
  headerExtra?: React.ReactNode
  footer?: React.ReactNode
}) {
  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-inner overflow-hidden border">
      <div className="p-6 border-b bg-muted/30 flex justify-between items-center">
        <div>
          <p className="text-[10px] font-bold uppercase text-muted-foreground tracking-widest">
            {subtitle || "Document"}
          </p>
          <h3 className="text-sm font-bold font-mono">{title}</h3>
        </div>
        <div className="flex items-center gap-2">{headerExtra}</div>
      </div>

      <div className="flex-1 min-h-[600px] bg-zinc-100 p-4 flex items-center justify-center overflow-auto">
        {children}
      </div>

      {footer && <div className="p-6 border-t bg-muted/10">{footer}</div>}
    </div>
  )
}

function ErrorDisplay({ id, message }: { id: string; message?: string }) {
  return (
    <InlineErrorFallback
      title="Document Not Found"
      message={
        message ||
        `We couldn't find the requested file (Ref: ${id}). It may have been deleted or the link is invalid.`
      }
    />
  )
}

// --- Loader Components (External) ---

function FileLoader({ id, receiptId }: { id?: string; receiptId?: string }) {
  // 1. Fetch the Document Metadata
  const {
    data: document,
    isLoading: isDocLoading,
    isError: isDocError,
  } = useQuery({
    queryKey: ["document-metadata", id, receiptId],
    queryFn: async () => {
      if (id) return DocumentsService.readDocumentById({ id })
      if (receiptId) {
        const docs = await DocumentsService.readDocuments({
          entityId: receiptId as any,
          entityType: "Receipt",
        })
        return docs.data[0] || null
      }
      return null
    },
  })

  // 2. Fetch Receipt Metadata (only if it's a receipt view)
  const { data: receipt, isLoading: isReceiptLoading } = useQuery({
    queryKey: ["receipt-metadata", receiptId],
    queryFn: async () =>
      receiptId
        ? ((await FinancialsService.readReceiptById({
            id: receiptId,
          })) as ReceiptPublic)
        : null,
    enabled: !!receiptId,
  })

  if (isDocLoading || isReceiptLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-24 text-center w-full">
        <Loader2 className="size-8 animate-spin text-primary mb-4" />
        <p className="text-muted-foreground">Loading document...</p>
      </div>
    )
  }

  if (isDocError || !document) {
    return <ErrorDisplay id={id || receiptId || "N/A"} />
  }

  const downloadUrl = DocumentService.getPdfUrl(document.id, "generic")

  const headerExtra = (
    <div className="flex items-center gap-4">
      {receipt && (
        <div className="flex gap-6 text-right border-r pr-4">
          <div>
            <p className="text-[10px] font-bold uppercase text-muted-foreground">
              Amount
            </p>
            <p className="font-bold text-xs">
              KES {receipt.amount.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-[10px] font-bold uppercase text-muted-foreground">
              Mode
            </p>
            <p className="font-bold text-xs">{receipt.mode}</p>
          </div>
        </div>
      )}
      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="sm"
          className="gap-2"
          onClick={() =>
            DocumentService.download({
              id: document.id,
              type: "generic",
              filename: document.document_type || "document",
            })
          }
        >
          <Download className="size-4" />
          Download
        </Button>
        <Button
          variant="outline"
          size="sm"
          className="gap-2"
          onClick={() => window.print()}
        >
          <Printer className="size-4" />
          Print
        </Button>
      </div>
    </div>
  )

  const footer =
    receipt?.allocations && receipt.allocations.length > 0 ? (
      <>
        <p className="text-[10px] font-bold uppercase text-muted-foreground mb-3 flex items-center gap-2">
          <FileText className="size-3" />
          Payment Allocations
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {receipt.allocations.map((alloc: any, i: number) => (
            <div
              key={i}
              className="flex justify-between text-xs bg-white p-2 rounded border border-black/5"
            >
              <span className="text-muted-foreground font-mono">
                {alloc.invoice_id.substring(0, 13)}...
              </span>
              <span className="font-bold">
                KES {alloc.amount_allocated.toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </>
    ) : undefined

  return (
    <DocumentShell
      title={document.document_type || "External File"}
      subtitle={receipt ? "Receipt Proof" : "Attachment"}
      headerExtra={headerExtra}
      footer={footer}
    >
      {document.mime_type?.startsWith("image/") ? (
        <img
          src={downloadUrl}
          alt={document.document_type}
          className="max-w-full h-auto shadow-2xl rounded-sm border bg-white"
        />
      ) : (
        <iframe
          src={downloadUrl}
          className="w-full h-full min-h-[800px] border-none shadow-2xl bg-white rounded-sm"
          title="Document Viewer"
        />
      )}
    </DocumentShell>
  )
}

// --- Main Component ---

export function DocumentViewer({ id, type }: DocumentViewerProps) {
  const isInternal = ["risknote", "invoice", "renewal"].includes(type)

  const docType = type as DocumentSourceType
  const htmlUrl = isInternal ? DocumentService.getHtmlUrl(id, docType) : ""
  const title =
    type === "risknote"
      ? "Risk Note"
      : type === "invoice"
        ? "Invoice"
        : type === "renewal"
          ? "Renewal Invitation"
          : "Document"

  const handleDownload = () => {
    DocumentService.download({ id, type: docType, title })
  }

  const headerExtra = isInternal ? (
    <div className="flex items-center gap-2">
      <Button
        variant="outline"
        size="sm"
        className="gap-2"
        onClick={handleDownload}
      >
        <Download className="size-4" />
        Download PDF
      </Button>
      <Button
        variant="outline"
        size="sm"
        className="gap-2"
        onClick={() => window.print()}
      >
        <Printer className="size-4" />
        Print
      </Button>
    </div>
  ) : null

  return (
    <div className="w-full h-full animate-in fade-in zoom-in-95 duration-300 flex flex-col gap-4">
      <div className="flex-1">
        {isInternal && (
          <DocumentShell
            title={title}
            subtitle="Internal Document"
            headerExtra={headerExtra}
          >
            <Suspense
              fallback={
                <div className="flex items-center justify-center p-24">
                  <Loader2 className="size-8 animate-spin text-primary" />
                </div>
              }
            >
              <HTMLViewer apiUrl={htmlUrl} title={title} />
            </Suspense>
          </DocumentShell>
        )}

        {!isInternal && (
          <>
            {type === "receipt" && <FileLoader receiptId={id} />}
            {type === "external" && <FileLoader id={id} />}
          </>
        )}
      </div>
    </div>
  )
}
