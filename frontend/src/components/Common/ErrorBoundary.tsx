import { AlertCircle } from "lucide-react"
import { Component, type ErrorInfo, type ReactNode } from "react"
import { Button } from "../ui/button"

interface Props {
  children?: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
  }

  public static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI.
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo)
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-background p-4 text-center">
          <div className="mb-4 rounded-full bg-destructive/10 p-3 text-destructive">
            <AlertCircle size={48} />
          </div>
          <h1 className="mb-2 text-2xl font-bold tracking-tight">
            Something went wrong
          </h1>
          <p className="mb-6 max-w-md text-muted-foreground">
            An unexpected error occurred. We've been notified and are working on
            a fix.
          </p>
          <div className="flex gap-4">
            <Button onClick={() => window.location.reload()}>
              Reload Page
            </Button>
            <Button
              variant="outline"
              onClick={() => {
                window.location.href = "/";
              }}
            >
              Go to Dashboard
            </Button>

          </div>
          {process.env.NODE_ENV === "development" && (
            <div className="mt-8 max-w-2xl overflow-auto rounded-md bg-muted p-4 text-left font-mono text-sm">
              <p className="mb-2 font-bold text-destructive">
                {this.state.error?.name}: {this.state.error?.message}
              </p>
              <pre className="whitespace-pre-wrap">
                {this.state.error?.stack}
              </pre>
            </div>
          )}
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
