import { createFileRoute } from "@tanstack/react-router"
import { Suspense, useCallback, useState } from "react"
import { PoliciesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { DocumentManager } from "@/components/Common/DocumentManager"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import ErrorComponent from "@/components/Common/ErrorComponent"
import { SummaryCard } from "@/components/Common/SummaryCard"
import { UniversalDocumentViewer } from "@/components/Documents/UniversalDocumentViewer"
import { RiskNoteForm } from "@/components/Insurance/RiskNoteForm"
import PendingItems from "@/components/Pending/PendingItems"
import { AssetCard } from "@/components/Policies/Dashboard/AssetCard"
import { CoverageCard } from "@/components/Policies/Dashboard/CoverageCard"

import { PolicyHeader } from "@/components/Policies/Dashboard/PolicyHeader"
import { getColumns as getRiskNoteColumns } from "@/components/RiskNotes/columns"
import { Badge } from "@/components/ui/badge"
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
  const { policy, latestRiskNote, activeItem, riskNotes, isLoading } =
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

  // Handlers
  const handleViewRiskNote = useCallback(
    (id: string, type: "risknote" | "invoice" = "risknote") => {
      setSelectedRiskNoteId(id)
      setViewType(type)
      setViewerOpen(true)
    },
    [],
  )

  const handleRenew = () => {
    setTransactionType("Renewal")
    setRiskNoteFormOpen(true)
  }

  const handleEndorse = () => {
    setTransactionType("Endorsement")
    setRiskNoteFormOpen(true)
  }

  if (isLoading || !policy || !client) {
    return <PendingItems />
  }

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
          <TabsTrigger value="history">Risk Notes</TabsTrigger>
          <TabsTrigger value="documents">Documents</TabsTrigger>
        </TabsList>

        {/* TAB 1: OVERVIEW */}
        <TabsContent value="overview" className="pt-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <SummaryCard
              title="Insured Value"
              value={`KES ${((latestRiskNote?.premium_breakdown as any)?.basic / 0.04 || 0).toLocaleString()}`}
              description="Current Sum Insured"
            />
            <SummaryCard
              title="Total Premium"
              value={`KES ${(latestRiskNote?.premium_breakdown as any)?.total?.toLocaleString() || "0.00"}`}
              description="Including Levies & Taxes"
            />
            <SummaryCard
              title="Period"
              value={`${latestRiskNote?.start_date || "N/A"}`}
              description={`To ${latestRiskNote?.end_date || "N/A"}`}
            />
            <SummaryCard
              title="Product"
              value={policy.product?.name || "N/A"}
              description={policy.product?.class_of_insurance || "Policy Type"}
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column (2/3) */}
            <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="h-full">
                <CoverageCard
                  riskNote={latestRiskNote}
                  onViewBreakdown={(rn) => handleViewRiskNote(rn.id, "invoice")}
                />
              </div>
              <div className="h-full">
                <AssetCard item={activeItem} />
              </div>
            </div>

            {/* Right Column (1/3) - Quick View Documents */}
            <div className="space-y-6">
              <Card className="bg-muted/20">
                <CardHeader>
                  <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
                    Financial Status
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">
                      Status
                    </span>
                    <Badge
                      variant="outline"
                      className="bg-green-500/10 text-green-600 border-green-200"
                    >
                      Paid
                    </Badge>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">
                      Balance
                    </span>
                    <span className="font-mono font-bold">KES 0.00</span>
                  </div>
                  <Button
                    variant="ghost"
                    className="w-full justify-start gap-2 text-primary"
                    onClick={() =>
                      latestRiskNote &&
                      handleViewRiskNote(latestRiskNote.id, "invoice")
                    }
                  >
                    View Latest Debit Note
                  </Button>
                </CardContent>
              </Card>
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
            ownerId={policy.client_id}
            ownerType="policy"
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
            <UniversalDocumentViewer id={selectedRiskNoteId} type={viewType} />
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
            initialTransactionType={transactionType}
            onSuccess={() => setRiskNoteFormOpen(false)}
            onCancel={() => setRiskNoteFormOpen(false)}
          />
        </DialogContent>
      </Dialog>
    </div>
  )
}
