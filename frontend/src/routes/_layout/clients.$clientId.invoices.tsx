import { createFileRoute } from "@tanstack/react-router"
import { ClientInvoices } from "@/components/Clients/ClientInvoices"

export const Route = createFileRoute("/_layout/clients/$clientId/invoices")({
  component: ClientInvoicesTab,
})

function ClientInvoicesTab() {
  const { clientId } = Route.useParams()
  return <ClientInvoices clientId={clientId} />
}
