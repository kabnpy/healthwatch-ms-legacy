import { useQuery } from "@tanstack/react-query"
import { AlertCircle, FileText, Loader2 } from "lucide-react"
import { Suspense, useState } from "react"

import {
  DocumentsService,
  FinancialsService,
  OpenAPI,
  type ReceiptPublic,
} from "@/client"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { BlobPDFViewer } from "../Common/BlobPDFViewer"
import { HTMLViewer } from "../Common/HTMLViewer"

// --- Types ---

type DocumentType = "risknote" | "invoice" | "receipt" | "external" | "renewal"

interface DocumentViewerProps {
  id: string
  type: DocumentType
  initialViewMode?: "digital" | "pdf"
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
        {headerExtra}
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
    <div className="flex flex-col items-center justify-center p-12 text-center bg-white rounded-lg shadow-inner border border-dashed m-8 w-full">
      <div className="p-4 rounded-full bg-destructive/10 text-destructive mb-4">
        <AlertCircle className="size-8" />
      </div>
      <h3 className="text-lg font-bold">Document Not Found</h3>
      <p className="text-muted-foreground max-w-xs mx-auto">
        {message ||
          "We couldn't find the requested file. It may have been deleted or the link is invalid."}
      </p>
      <p className="text-[10px] text-muted-foreground mt-4 font-mono">
        Reference ID: {id}
      </p>
    </div>
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

  const baseUrl = OpenAPI.BASE || "http://localhost:8000"
  const downloadUrl = `${baseUrl.replace(/\/$/, "")}/api/v1/documents/${document.id}/download`

  const headerExtra = receipt ? (
    <div className="flex gap-6 text-right">
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
  ) : null

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
      ) : document.mime_type === "application/pdf" ? (
        <BlobPDFViewer url={downloadUrl} title="Document Viewer" />
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

export function DocumentViewer({
  id,
  type,
  initialViewMode = "digital",
}: DocumentViewerProps) {
  const [viewMode, setViewMode] = useState<"digital" | "pdf">(initialViewMode)

  const baseUrl = (OpenAPI.BASE || "").replace(/\/$/, "")
  const isInternal = ["risknote", "invoice", "renewal"].includes(type)

  let htmlUrl = ""
  let pdfUrl = ""
  let title = ""

  if (type === "risknote") {
    htmlUrl = `${baseUrl}/api/v1/risk-notes/${id}/html`
    pdfUrl = `${baseUrl}/api/v1/risk-notes/${id}/pdf`
    title = "Risk Note"
  } else if (type === "invoice") {
    htmlUrl = `${baseUrl}/api/v1/financials/invoices/${id}/html`
    pdfUrl = `${baseUrl}/api/v1/financials/invoices/${id}/pdf`
    title = "Invoice"
  } else if (type === "renewal") {
    htmlUrl = `${baseUrl}/api/v1/policies/${id}/renewal-invitation/html`
    pdfUrl = `${baseUrl}/api/v1/policies/${id}/renewal-invitation/pdf`
    title = "Renewal Invitation"
  }

  return (
    <div className="w-full h-full animate-in fade-in zoom-in-95 duration-300 flex flex-col gap-4">
      {isInternal && (
        <div className="flex justify-center">
          <Tabs
            value={viewMode}
            onValueChange={(v) => setViewMode(v as any)}
            className="w-auto"
          >
            <TabsList>
              <TabsTrigger
                value="digital"
                className="text-xs font-bold uppercase"
              >
                Digital Version
              </TabsTrigger>
              <TabsTrigger value="pdf" className="text-xs font-bold uppercase">
                PDF Version (Official)
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      )}

      <div className="flex-1">
        {isInternal && (
          <Suspense
            fallback={
              <div className="flex items-center justify-center p-24">
                <Loader2 className="size-8 animate-spin text-primary" />
              </div>
            }
          >
            {viewMode === "digital" ? (
              <HTMLViewer apiUrl={htmlUrl} title={title} />
            ) : (
              <div className="w-full h-full bg-zinc-100 flex items-center justify-center p-4">
                <BlobPDFViewer url={pdfUrl} title={`${title} PDF`} />
              </div>
            )}
          </Suspense>
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
