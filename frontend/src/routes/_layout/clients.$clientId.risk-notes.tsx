import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Suspense, useMemo, useState } from "react"
import { PoliciesService, RiskNotesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { DocumentViewerModal } from "@/components/Common/DocumentViewerModal"
import { RiskNoteDocument } from "@/components/Documents/RiskNoteDocument"
import PendingItems from "@/components/Pending/PendingItems"
import { getColumns as getRiskNoteColumns } from "@/components/RiskNotes/columns"

function getPoliciesQueryOptions(clientId: string) {
  return {
    queryFn: () =>
      PoliciesService.readPolicies({ clientId, skip: 0, limit: 100 }),
    queryKey: ["policies", { clientId }],
  }
}

function getClientRiskNotesQueryOptions() {
  return {
    queryFn: () => RiskNotesService.readRiskNotes({ skip: 0, limit: 1000 }),
    queryKey: ["risk-notes"],
  }
}

export const Route = createFileRoute("/_layout/clients/$clientId/risk-notes")({
  component: ClientRiskNotes,
})

function ClientRiskNotes() {
  const { clientId } = Route.useParams()
  const { data: policies } = useSuspenseQuery(getPoliciesQueryOptions(clientId))
  const { data: allRiskNotes } = useSuspenseQuery(
    getClientRiskNotesQueryOptions(),
  )

  const [viewerOpen, setViewerOpen] = useState(false)
  const [selectedRiskNoteId, setSelectedRiskNoteId] = useState<string | null>(
    null,
  )
  const [viewMode, setViewMode] = useState<"invoice" | "certificate">("invoice")

  const policyIds = new Set(policies.data.map((p) => p.id))
  const clientRiskNotes = allRiskNotes.data.filter((rn) =>
    policyIds.has(rn.policy_id),
  )

  const riskNoteColumns = useMemo(
    () =>
      getRiskNoteColumns((riskNote) => {
        setSelectedRiskNoteId(riskNote.id)
        setViewMode("invoice")
        setViewerOpen(true)
      }),
    [],
  )

  return (
    <div className="space-y-4 pt-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-tight">Recent Risk Notes</h2>
      </div>
      {clientRiskNotes.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-12 border rounded-lg bg-muted/5">
          <h3 className="text-lg font-semibold">No risk notes yet</h3>
          <p className="text-muted-foreground">
            Financial transactions will appear here once policies are active
          </p>
        </div>
      ) : (
        <DataTable columns={riskNoteColumns} data={clientRiskNotes} />
      )}

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
