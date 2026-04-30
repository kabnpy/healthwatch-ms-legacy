import { OpenAPI } from "@/client"
import { downloadAuthenticatedFile } from "@/utils/insurance"

export type DocumentSourceType = "risknote" | "invoice" | "renewal" | "generic"

export interface DocumentInfo {
  id: string
  type: DocumentSourceType
  title?: string
  filename?: string
}

function getBaseUrl(): string {
  return (OpenAPI.BASE || "").replace(/\/$/, "")
}

/**
 * Constructs the authenticated PDF download/view URL.
 */
export function getPdfUrl(id: string, type: DocumentSourceType): string {
  const baseUrl = getBaseUrl()
  switch (type) {
    case "risknote":
      return `${baseUrl}/api/v1/risk-notes/${id}/pdf`
    case "invoice":
      return `${baseUrl}/api/v1/financials/invoices/${id}/pdf`
    case "renewal":
      return `${baseUrl}/api/v1/policies/${id}/renewal-invitation/pdf`
    case "generic":
      return `${baseUrl}/api/v1/documents/${id}/download`
    default:
      throw new Error(`Unsupported document type: ${type}`)
  }
}

/**
 * Constructs the HTML preview URL (where supported).
 */
export function getHtmlUrl(id: string, type: DocumentSourceType): string {
  const baseUrl = getBaseUrl()
  switch (type) {
    case "risknote":
      return `${baseUrl}/api/v1/risk-notes/${id}/html`
    case "renewal":
      return `${baseUrl}/api/v1/policies/${id}/renewal-invitation/html`
    default:
      // Fallback to PDF URL for types that don't have HTML routes
      return getPdfUrl(id, type)
  }
}

/**
 * Orchestrates an authenticated download of a PDF document.
 */
export async function downloadDocument(info: DocumentInfo): Promise<void> {
  const url = getPdfUrl(info.id, info.type)
  const filename =
    info.filename ||
    `${info.title?.replace(/\s+/g, "_") || info.type}_${info.id.substring(0, 8)}.pdf`
  return downloadAuthenticatedFile(url, filename)
}

export const DocumentService = {
  getPdfUrl,
  getHtmlUrl,
  download: downloadDocument,
}
