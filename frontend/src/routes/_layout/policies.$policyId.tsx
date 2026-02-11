import { createFileRoute } from "@tanstack/react-router"
import { Clock, FileDown, Mail } from "lucide-react"
import { Suspense, useCallback, useState } from "react"
import { PoliciesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { DocumentManager } from "@/components/Common/DocumentManager"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import ErrorComponent from "@/components/Common/ErrorComponent"
import { DocumentViewer } from "@/components/Documents/DocumentViewer"
import { RiskNoteTemplate } from "@/components/Documents/templates/RiskNoteTemplate"
import { RiskNoteForm } from "@/components/Insurance/RiskNoteForm"
import PendingItems from "@/components/Pending/PendingItems"
import { PolicyHeader } from "@/components/Policies/Dashboard/PolicyHeader"
import { getColumns as getRiskNoteColumns } from "@/components/RiskNotes/columns"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useClient, usePolicyDashboard } from "@/hooks/useInsurance"
import { queryClient } from "@/queryClient"
import type { EnhancedRiskNote, EnhancedPolicy } from "@/types/insurance"

// --- Route Definition ---

export const Route = createFileRoute("/_layout/policies/$policyId")({
  component: PolicyDashboard,
  errorComponent: ErrorComponent,
  loader: ({ params }) =>
    queryClient.ensureQueryData({
      queryKey: ["policy", params.policyId],
      queryFn: () => PoliciesService.readPolicy({ id: params.policyId }),
    }),
})

// --- Main Page Component ---

function PolicyDashboard() {
  const { policyId } = Route.useParams()

  return (
    <Suspense fallback={<PendingItems />}>
      <PolicyDashboardContent policyId={policyId} />
    </Suspense>
  )
}

// --- Component Content (Suspended) ---

function PolicyDashboardContent({ policyId }: { policyId: string }) {
  const { policy, latestRiskNote, riskNotes, isLoading } =
    usePolicyDashboard(policyId)

  // We need client name for breadcrumbs
  const { data: client } = useClient(policy?.client_id || "")

  // State for Document Viewer
  const [viewerOpen, setViewerOpen] = useState(false)
  const [selectedRiskNoteId, setSelectedRiskNoteId] = useState<string | null>(
    null,
  )
  const [viewType, setViewType] = useState<"risknote" | "invoice">("risknote")

  // State for Risk Note Form
  const [riskNoteFormOpen, setRiskNoteFormOpen] = useState(false)
  const [transactionType, setTransactionType] = useState("Endorsement")
  const [editingRiskNoteId, setEditingRiskNoteId] = useState<
    string | undefined
  >()

  // Handlers
  const handleViewRiskNote = useCallback(
    (id: string, type: "risknote" | "invoice" = "risknote") => {
      setSelectedRiskNoteId(id)
      setViewType(type)
      setViewerOpen(true)
    },
    [],
  )

  const handlePopulateDraft = () => {
    if (latestRiskNote?.id) {
      setTransactionType(latestRiskNote.transaction_type)
      setEditingRiskNoteId(latestRiskNote.id)
      setRiskNoteFormOpen(true)
    }
  }

  const handleRenew = () => {
    setTransactionType("Renewal")
    setEditingRiskNoteId(undefined)
    setRiskNoteFormOpen(true)
  }

  const handleEndorse = () => {
    setTransactionType("Endorsement")
    setEditingRiskNoteId(undefined)
    setRiskNoteFormOpen(true)
  }

  if (isLoading || !policy || !client) {
    return <PendingItems />
  }

  const daysToExpiry = latestRiskNote
    ? Math.ceil(
        (new Date(latestRiskNote.end_date).getTime() - Date.now()) /
          (1000 * 60 * 60 * 24),
      )
    : 0

  return (
    <div className="flex flex-col gap-6">
      <PolicyHeader
        clientName={client.name}
        clientId={client.id}
        policyNumber={policy.policy_number}
        displayName={policy.display_name}
        status={policy.status || "Unknown"}
        onRenew={handleRenew}
        onEndorse={handleEndorse}
      />

      <Tabs defaultValue="overview" className="w-full">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
          <TabsTrigger value="documents">Documents</TabsTrigger>
        </TabsList>

        {/* TAB 1: OVERVIEW (The Digital File) */}
        <TabsContent value="overview" className="pt-6">
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 items-start">
            {/* Main Column: The Document */}
            <div className="lg:col-span-3 space-y-6">
              {(latestRiskNote as any)?.status === "Draft" && (
                <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg flex items-center justify-between shadow-sm">
                  <div className="flex items-center gap-3">
                    <div className="bg-blue-500 p-2 rounded-full">
                      <FileDown className="size-4 text-white" />
                    </div>
                    <div>
                      <p className="text-sm font-bold text-blue-900">
                        Draft Risk Note Detected
                      </p>
                      <p className="text-xs text-blue-700">
                        This {latestRiskNote?.transaction_type} has not been
                        finalized yet.
                      </p>
                    </div>
                  </div>
                  <Button
                    size="sm"
                    className="bg-blue-600 hover:bg-blue-700 text-white gap-2"
                    onClick={handlePopulateDraft}
                  >
                    Populate & Issue
                  </Button>
                </div>
              )}

              {latestRiskNote ? (
                <div className="border rounded-lg shadow-xl overflow-hidden bg-white dark:bg-zinc-950">
                  <div className="p-1 bg-muted/20 border-b text-[10px] uppercase tracking-widest text-center text-muted-foreground font-semibold">
                    Current Master Risk Note
                  </div>
                  <RiskNoteTemplate
                    riskNote={latestRiskNote as EnhancedRiskNote}
                    client={client}
                    policy={policy as EnhancedPolicy}
                  />
                </div>
              ) : (
                <div className="p-12 text-center border-2 border-dashed rounded-lg bg-muted/10">
                  <p className="text-muted-foreground italic">
                    No transaction history found for this policy.
                  </p>
                </div>
              )}
            </div>

            {/* Sidebar: Live Data & Quick Actions */}
            <div className="lg:col-span-1 space-y-6">
              {/* Live Expiry Sidebar Card */}
              <Card className="border-l-4 border-l-blue-500 shadow-sm">
                <CardHeader className="pb-2">
                  <CardTitle className="text-xs font-bold uppercase text-muted-foreground flex items-center gap-2">
                    <Clock className="size-3" />
                    Status Tracker
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="text-2xl font-bold">{daysToExpiry}</div>
                    <p className="text-[10px] text-muted-foreground uppercase tracking-tighter">
                      Days until Expiry
                    </p>
                  </div>
                  <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className={`h-full ${daysToExpiry < 30 ? "bg-destructive" : "bg-blue-500"}`}
                      style={{
                        width: `${Math.min(100, (daysToExpiry / 365) * 100)}%`,
                      }}
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Document Quick Actions */}
              <div className="space-y-2">
                <h4 className="text-[10px] font-bold uppercase text-muted-foreground px-1 tracking-widest">
                  Print / Export
                </h4>
                <Button
                  variant="outline"
                  className="w-full justify-start gap-3 h-10 shadow-sm group"
                >
                  <FileDown className="size-4 text-muted-foreground group-hover:text-primary" />
                  <span className="text-xs">Download PDF</span>
                </Button>
                <Button
                  variant="outline"
                  className="w-full justify-start gap-3 h-10 shadow-sm group"
                >
                  <Mail className="size-4 text-muted-foreground group-hover:text-primary" />
                  <span className="text-xs">Email to Client</span>
                </Button>
              </div>
            </div>
          </div>
        </TabsContent>

        {/* TAB 2: HISTORY (Risk Notes) */}

        <TabsContent value="history" className="pt-6">
          <div className="border rounded-lg p-4 bg-card">
            <h3 className="text-lg font-semibold mb-4 text-primary">
              Transaction History (Risk Notes)
            </h3>

            <DataTable
              columns={getRiskNoteColumns((rn) =>
                handleViewRiskNote(rn.id, "risknote"),
              )}
              data={riskNotes}
            />
          </div>
        </TabsContent>

        {/* TAB 4: DOCUMENTS */}
        <TabsContent value="documents" className="pt-6">
          <DocumentManager
            entityId={policyId}
            entityType="Policy"
            title="Policy Support Documents"
          />
        </TabsContent>
      </Tabs>

      {/* Document Viewer Modal */}
      {selectedRiskNoteId && (
        <DocumentViewerModal
          isOpen={viewerOpen}
          onClose={() => setViewerOpen(false)}
          title={`Document: ${selectedRiskNoteId}`}
        >
          <Suspense fallback={<PendingItems />}>
            <DocumentViewer id={selectedRiskNoteId} type={viewType} />
          </Suspense>
        </DocumentViewerModal>
      )}

      {/* Risk Note Form Dialog (Renewals/Endorsements) */}
      <Dialog open={riskNoteFormOpen} onOpenChange={setRiskNoteFormOpen}>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>
              {transactionType} for Policy {policy.policy_number}
            </DialogTitle>
            <DialogDescription>
              Create a new financial transaction for this policy.
            </DialogDescription>
          </DialogHeader>
          <RiskNoteForm
            policyId={policyId}
            riskNoteId={editingRiskNoteId}
            onSuccess={() => setRiskNoteFormOpen(false)}
            onCancel={() => setRiskNoteFormOpen(false)}
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}
