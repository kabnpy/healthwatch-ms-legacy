import { MutationCache, QueryCache, QueryClient } from "@tanstack/react-query"
import { toast } from "sonner"
import { ApiError } from "./client"

const handleApiError = (error: Error) => {
  if (error instanceof ApiError) {
    if ([401, 403].includes(error.status)) {
      localStorage.removeItem("access_token")
      window.location.href = "/login"
      return
    }

    const message =
      (error.body as any)?.detail ||
      error.message ||
      "An unexpected error occurred"
    toast.error("API Error", {
      description: message,
    })
  } else {
    toast.error("System Error", {
      description: error.message || "An unexpected system error occurred",
    })
  }
}

export const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: handleApiError,
  }),
  mutationCache: new MutationCache({
    onError: handleApiError,
  }),
  defaultOptions: {
    queries: {
      retry: (failureCount, error: any) => {
        // Don't retry on 401, 403, 404
        if (
          error instanceof ApiError &&
          [401, 403, 404].includes(error.status)
        ) {
          return false
        }
        return failureCount < 2
      },
    },
  },
})
