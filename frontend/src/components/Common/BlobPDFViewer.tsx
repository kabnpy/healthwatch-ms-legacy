import { Loader2 } from "lucide-react"
import { useEffect, useState } from "react"

interface BlobPDFViewerProps {
  url: string
  className?: string
  title?: string
}

export function BlobPDFViewer({
  url,
  className = "w-full h-full min-h-[800px]",
  title = "PDF Viewer",
}: BlobPDFViewerProps) {
  const [blobUrl, setBlobUrl] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    let active = true
    const token = localStorage.getItem("access_token")

    const fetchPDF = async () => {
      try {
        setIsLoading(true)
        const response = await fetch(url, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })

        if (!response.ok) {
          throw new Error(`Failed to fetch PDF: ${response.statusText}`)
        }

        const blob = await response.blob()
        if (active) {
          const objectUrl = URL.createObjectURL(blob)
          setBlobUrl(objectUrl)
          setIsLoading(false)
        }
      } catch (err: any) {
        if (active) {
          setError(err.message)
          setIsLoading(false)
        }
      }
    }

    fetchPDF()

    return () => {
      active = false
    }
  }, [url])

  // Cleanup blob URL when component unmounts or blobUrl changes
  useEffect(() => {
    return () => {
      if (blobUrl) {
        URL.revokeObjectURL(blobUrl)
      }
    }
  }, [blobUrl])

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center p-12 w-full h-full bg-muted/5 rounded-lg border border-dashed">
        <Loader2 className="size-8 animate-spin text-primary mb-4" />
        <p className="text-sm text-muted-foreground font-medium">
          Generating PDF...
        </p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center p-12 w-full h-full bg-destructive/5 rounded-lg border border-destructive/20">
        <p className="text-sm text-destructive font-bold mb-2">
          Authentication Error
        </p>
        <p className="text-xs text-muted-foreground text-center max-w-xs">
          {error}. Please try logging in again if the issue persists.
        </p>
      </div>
    )
  }

  if (!blobUrl) return null

  return (
    <iframe
      src={blobUrl}
      className={`${className} border shadow-lg bg-white rounded-sm`}
      title={title}
    />
  )
}
