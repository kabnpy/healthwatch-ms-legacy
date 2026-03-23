import { Loader2 } from "lucide-react"
import { useEffect, useState } from "react"
import { OpenAPI } from "@/client"

interface HTMLRiskNoteViewerProps {
  riskNoteId: string
  className?: string
}

export function HTMLRiskNoteViewer({
  riskNoteId,
  className = "w-full h-full min-h-[800px]",
}: HTMLRiskNoteViewerProps) {
  const [htmlContent, setHtmlContent] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let active = true
    const token = localStorage.getItem("access_token")
    const url = `${(OpenAPI.BASE || "").replace(/\/$/, "")}/api/v1/risk-notes/${riskNoteId}/html`

    const fetchHTML = async () => {
      try {
        setIsLoading(true)
        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          throw new Error(`Failed to fetch Risk Note: ${response.statusText}`)
        }

        const text = await response.text()
        if (active) {
          setHtmlContent(text)
          setIsLoading(false)
        }
      } catch (err: any) {
        if (active) {
          setError(err.message)
          setIsLoading(false)
        }
      }
    }

    fetchHTML()

    return () => {
      active = false
    }
  }, [riskNoteId])

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 w-full h-full bg-muted/5 rounded-lg border border-dashed">
        <Loader2 className="size-8 animate-spin text-primary mb-4" />
        <p className="text-sm text-muted-foreground font-medium">
          Loading Document...
        </p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-12 w-full h-full bg-destructive/5 rounded-lg border border-destructive/20">
        <p className="text-sm text-destructive font-bold mb-2">
          Error Loading Document
        </p>
        <p className="text-xs text-muted-foreground text-center max-w-xs">
          {error}
        </p>
      </div>
    )
  }

  if (!htmlContent) return null

  return (
    <div className={`${className} bg-white shadow-sm border rounded-sm overflow-auto`}>
      <div 
        dangerouslySetInnerHTML={{ __html: htmlContent }} 
        className="p-8 print:p-0"
      />
    </div>
  )
}
