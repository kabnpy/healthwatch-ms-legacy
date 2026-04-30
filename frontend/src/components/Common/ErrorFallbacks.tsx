import { AlertCircle, RefreshCw } from "lucide-react"
import { Button } from "../ui/button"

interface FallbackProps {
  reset?: () => void
  title?: string
  message?: string
}

/**
 * Standardized error fallback for inline sections and cards.
 */
export function InlineErrorFallback({ reset, title, message }: FallbackProps) {
  return (
    <div className="flex flex-col items-center justify-center p-8 text-center bg-destructive/5 rounded-lg border border-destructive/20 border-dashed w-full min-h-[150px]">
      <AlertCircle className="size-8 text-destructive mb-2" />
      <h3 className="text-sm font-bold">{title || "Failed to load content"}</h3>
      <p className="text-xs text-muted-foreground mb-4 max-w-[250px]">
        {message || "This section couldn't be loaded correctly."}
      </p>
      {reset && (
        <Button size="sm" variant="outline" onClick={reset} className="gap-2">
          <RefreshCw className="size-3" />
          Retry
        </Button>
      )}
    </div>
  )
}

/**
 * Compact error fallback for smaller UI elements or sidebar cards.
 */
export function CardErrorFallback({ title, reset }: FallbackProps) {
  return (
    <div className="h-full min-h-[200px] flex flex-col items-center justify-center p-6 text-center border rounded-xl bg-muted/5 w-full">
      <AlertCircle className="size-6 text-muted-foreground mb-2" />
      <h3 className="text-sm font-semibold">{title || "Data"} unavailable</h3>
      <p className="text-xs text-muted-foreground mb-4">
        Try refreshing the component.
      </p>
      {reset && (
        <Button
          size="xs"
          variant="ghost"
          onClick={reset}
          className="text-[10px] uppercase tracking-widest font-bold"
        >
          Reload
        </Button>
      )}
    </div>
  )
}

/**
 * Full page error fallback for route-level boundaries.
 */
export function PageErrorFallback({ reset }: FallbackProps) {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center p-8 text-center">
      <div className="mb-6 rounded-full bg-destructive/10 p-4 text-destructive">
        <AlertCircle className="size-12" />
      </div>
      <h1 className="mb-2 text-2xl font-bold tracking-tight text-zinc-900">
        Oops! Something went wrong
      </h1>
      <p className="mb-8 max-w-md text-muted-foreground">
        We encountered an error while trying to display this page.
      </p>
      <div className="flex gap-4">
        {reset && (
          <Button onClick={reset} size="lg">
            Try Again
          </Button>
        )}
        <Button
          variant="outline"
          size="lg"
          onClick={() => {
            window.location.href = "/"
          }}
        >
          Return Home
        </Button>
      </div>
    </div>
  )
}
