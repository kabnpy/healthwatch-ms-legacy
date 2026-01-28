import { useSuspenseQuery } from "@tanstack/react-query"
import {
  createFileRoute,
  Link,
  Outlet,
  useLocation,
} from "@tanstack/react-router"
import { User } from "lucide-react"
import { Suspense } from "react"
import { ClientsService } from "@/client"
import ErrorComponent from "@/components/Common/ErrorComponent"
import PendingItems from "@/components/Pending/PendingItems"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
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
  const activeTab = location.pathname.split("/").pop() || "policies"

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{client.name}</h1>
        <p className="text-muted-foreground">
          Client Hub - manage details and policies
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">KRA PIN</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{client.kra_pin}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Email</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-sm truncate">{client.email || "N/A"}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Phone</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{client.phone}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Type</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{client.client_type}</div>
          </CardContent>
        </Card>
      </div>

      <Tabs value={activeTab} className="w-full">
        <TabsList>
          <TabsTrigger value="policies" asChild>
            <Link to="/clients/$clientId/policies" params={{ clientId }}>
              Policies
            </Link>
          </TabsTrigger>
          <TabsTrigger value="risk-notes" asChild>
            <Link to="/clients/$clientId/risk-notes" params={{ clientId }}>
              Risk Notes
            </Link>
          </TabsTrigger>
          <TabsTrigger value="documents" asChild>
            <Link to="/clients/$clientId/documents" params={{ clientId }}>
              Documents
            </Link>
          </TabsTrigger>
        </TabsList>
        <Outlet />
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
