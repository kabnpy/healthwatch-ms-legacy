import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { User, Users } from "lucide-react"
import { Suspense, useMemo, useState } from "react"

import { ClientsService, PoliciesService, RiskNotesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import ErrorComponent from "@/components/Common/ErrorComponent"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import { RiskNoteDocument } from "@/components/Documents/RiskNoteDocument"
import { columns as policyColumns } from "@/components/Policies/columns"
import { getColumns as getRiskNoteColumns } from "@/components/RiskNotes/columns"
import { NewBusinessWizard } from "@/components/Insurance/Wizard/NewBusinessWizard"
import { Button } from "@/components/ui/button"
import PendingItems from "@/components/Pending/PendingItems"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Plus } from "lucide-react"

// --- Query Options ---

function getClientQueryOptions(clientId: string) {
  return {
    queryFn: () => ClientsService.readClient({ id: clientId }),
    queryKey: ["clients", clientId],
  }
}

function getPoliciesQueryOptions(clientId: string) {
  return {
    queryFn: () => PoliciesService.readPolicies({ clientId, skip: 0, limit: 100 }),
    queryKey: ["policies", { clientId }],
  }
}

function getClientRiskNotesQueryOptions() {
  return {
    queryFn: () => RiskNotesService.readRiskNotes({ skip: 0, limit: 1000 }),
    queryKey: ["risk-notes"],
  }
}

// --- Route Definition ---

export const Route = createFileRoute("/_layout/clients/$clientId")({
  component: ClientHub,
  errorComponent: ErrorComponent,
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
  const { data: policies } = useSuspenseQuery(getPoliciesQueryOptions(clientId))
  const { data: allRiskNotes } = useSuspenseQuery(getClientRiskNotesQueryOptions())

  // State for Document Viewer
  const [viewerOpen, setViewerOpen] = useState(false)
  const [selectedRiskNoteId, setSelectedRiskNoteId] = useState<string | null>(null)
  const [viewMode, setViewMode] = useState<"invoice" | "certificate">("invoice")

  // State for Wizard
  const [wizardOpen, setWizardOpen] = useState(false)

  // Filtering risk notes for this client
  const policyIds = new Set(policies.data.map((p) => p.id))
  const clientRiskNotes = allRiskNotes.data.filter((rn) => policyIds.has(rn.policy_id))

  // Memoize columns to pass the view handler
  const riskNoteColumns = useMemo(() => getRiskNoteColumns((riskNote) => {
    setSelectedRiskNoteId(riskNote.id)
    setViewMode("invoice")
    setViewerOpen(true)
  }), [])

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{client.name}</h1>
        <p className="text-muted-foreground">Client Hub - manage details and policies</p>
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

      <Tabs defaultValue="policies" className="w-full">
        <TabsList>
          <TabsTrigger value="policies">Policies</TabsTrigger>
          <TabsTrigger value="risk-notes">Risk Notes</TabsTrigger>
          <TabsTrigger value="correspondence">Correspondence</TabsTrigger>
        </TabsList>
        <TabsContent value="policies" className="space-y-4 pt-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold tracking-tight">Policies</h2>
            <Button onClick={() => setWizardOpen(true)} className="gap-2">
              <Plus className="size-4" />
              New Business Wizard
            </Button>
          </div>
          {policies.data.length === 0 ? (
            <div className="flex flex-col items-center justify-center text-center py-12 border rounded-lg bg-muted/5">
              <div className="rounded-full bg-muted p-4 mb-4">
                <Users className="h-8 w-8 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-semibold">No policies found</h3>
              <p className="text-muted-foreground">Create a new policy using the wizard</p>
            </div>
          ) : (
            <DataTable columns={policyColumns} data={policies.data} />
          )}
        </TabsContent>
        <TabsContent value="risk-notes" className="space-y-4 pt-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold tracking-tight">Recent Risk Notes</h2>
          </div>
          {clientRiskNotes.length === 0 ? (
            <div className="flex flex-col items-center justify-center text-center py-12 border rounded-lg bg-muted/5">
              <h3 className="text-lg font-semibold">No risk notes yet</h3>
              <p className="text-muted-foreground">Financial transactions will appear here once policies are active</p>
            </div>
          ) : (
            <DataTable columns={riskNoteColumns} data={clientRiskNotes} />
          )}
        </TabsContent>
        <TabsContent value="correspondence" className="pt-4">
          <div className="flex flex-col items-center justify-center text-center py-12 border rounded-lg bg-muted/10">
            <h3 className="text-lg font-semibold">No correspondence yet</h3>
            <p className="text-muted-foreground">Logs and documents will appear here</p>
          </div>
        </TabsContent>
      </Tabs>

      {/* Wizard Modal */}
      <NewBusinessWizard 
        clientId={clientId}
        isOpen={wizardOpen}
        onClose={() => setWizardOpen(false)}
      />

      {/* Document Viewer Modal */}
      {selectedRiskNoteId && (
        <DocumentViewerModal
          isOpen={viewerOpen}
          onClose={() => setViewerOpen(false)}
          title={`Risk Note: ${selectedRiskNoteId}`}
        >
          <Suspense fallback={<PendingItems />}>
            <RiskNoteDocument 
              id={selectedRiskNoteId} 
              mode={viewMode}
              onModeChange={setViewMode}
            />
          </Suspense>
        </DocumentViewerModal>
      )}
    </div>
  )
}

// --- Main Page Component ---

function ClientHub() {
  const { clientId } = Route.useParams()

  return (
    <Suspense fallback={<PendingItems />}>
      <ClientHubContent clientId={clientId} />
    </Suspense>
  )
}