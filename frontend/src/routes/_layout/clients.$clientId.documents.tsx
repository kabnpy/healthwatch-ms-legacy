import { createFileRoute } from "@tanstack/react-router"
import { ClientDocuments } from "@/components/Clients/ClientDocuments"

export const Route = createFileRoute("/_layout/clients/$clientId/documents")({
  component: ClientDocumentsTab,
})

function ClientDocumentsTab() {
  const { clientId } = Route.useParams()
  return (
    <div className="pt-4">
      <ClientDocuments clientId={clientId} />
    </div>
  )
}
