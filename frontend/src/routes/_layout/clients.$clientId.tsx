import { useSuspenseQuery } from "@tanstack/react-query"
import {
  createFileRoute,
  Link,
  Outlet,
  useLocation,
} from "@tanstack/react-router"
import { Suspense } from "react"
import { ClientsService } from "@/client"
import ErrorComponent from "@/components/Common/ErrorComponent"
import PendingItems from "@/components/Pending/PendingItems"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { queryClient } from "@/queryClient"

// --- Query Options ---

function getClientQueryOptions(clientId: string) {
  return {
    queryFn: () => ClientsService.readClient({ id: clientId }),
    queryKey: ["clients", clientId],
  }
}

// --- Route Definition ---

export const Route = createFileRoute("/_layout/clients/$clientId")({
  component: ClientHubLayout,
  errorComponent: ErrorComponent,
  loader: ({ params }) =>
    queryClient.ensureQueryData(getClientQueryOptions(params.clientId)),
  head: ({ params }) => ({
    meta: [
      {
        title: `Client Details - ${params.clientId}`,
      },
    ],
  }),
})

// --- Component Content (Suspended) ---

function ClientHubContent({ clientId }: { clientId: string }) {
  const { data: client } = useSuspenseQuery(getClientQueryOptions(clientId))
  const location = useLocation()

  // Determine active tab based on path
  const activeTab = location.pathname.split("/").pop() || "overview"

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">{client.name}</h1>
          <p className="text-sm text-muted-foreground uppercase tracking-wider font-semibold">
            {client.client_type} &bull; Client Hub
          </p>
        </div>
      </div>

      <Tabs value={activeTab} className="w-full">
        <TabsList>
          <TabsTrigger value="overview" asChild>
            <Link to="/clients/$clientId/overview" params={{ clientId }}>
              Overview
            </Link>
          </TabsTrigger>
          <TabsTrigger value="policies" asChild>
            <Link to="/clients/$clientId/policies" params={{ clientId }}>
              Policies
            </Link>
          </TabsTrigger>
          <TabsTrigger value="invoices" asChild>
            <Link to="/clients/$clientId/invoices" params={{ clientId }}>
              Invoices
            </Link>
          </TabsTrigger>
          <TabsTrigger value="documents" asChild>
            <Link to="/clients/$clientId/documents" params={{ clientId }}>
              Documents
            </Link>
          </TabsTrigger>
          <TabsTrigger value="settings" asChild>
            <Link to="/clients/$clientId/settings" params={{ clientId }}>
              Settings
            </Link>
          </TabsTrigger>
        </TabsList>
        <div className="mt-4">
          <Outlet />
        </div>
      </Tabs>
    </div>
  )
}

// --- Main Page Component ---

function ClientHubLayout() {
  const { clientId } = Route.useParams()

  return (
    <Suspense fallback={<PendingItems />}>
      <ClientHubContent clientId={clientId} />
    </Suspense>
  )
}
