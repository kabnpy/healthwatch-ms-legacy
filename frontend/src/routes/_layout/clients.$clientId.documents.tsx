import { createFileRoute } from "@tanstack/react-router"
import { DocumentManager } from "@/components/Common/DocumentManager"

export const Route = createFileRoute("/_layout/clients/$clientId/documents")({
  component: ClientDocumentsTab,
})

function ClientDocumentsTab() {
  const { clientId } = Route.useParams()
  return (
    <div className="pt-4">
      <DocumentManager
        entityId={clientId}
        entityType="Client"
        title="KYC & Legal Documents"
      />
    </div>
  )
}
