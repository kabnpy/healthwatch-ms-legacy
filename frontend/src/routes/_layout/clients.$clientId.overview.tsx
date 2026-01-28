import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Hash, Mail, Phone, User } from "lucide-react"
import { ClientsService } from "@/client"
import { SummaryCard } from "@/components/Common/SummaryCard"

function getClientQueryOptions(clientId: string) {
  return {
    queryFn: () => ClientsService.readClient({ id: clientId }),
    queryKey: ["clients", clientId],
  }
}

export const Route = createFileRoute("/_layout/clients/$clientId/overview")({
  component: ClientOverview,
})

function ClientOverview() {
  const { clientId } = Route.useParams()
  const { data: client } = useSuspenseQuery(getClientQueryOptions(clientId))

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4 pt-4">
      <SummaryCard
        title="KRA PIN"
        value={client.kra_pin}
        icon={Hash}
        valueClassName="font-mono text-xl"
      />
      <SummaryCard
        title="Email Address"
        value={client.email || "N/A"}
        icon={Mail}
        valueClassName="text-sm truncate"
      />
      <SummaryCard
        title="Phone Number"
        value={client.phone}
        icon={Phone}
        valueClassName="text-xl"
      />
      <SummaryCard
        title="Client Type"
        value={client.client_type}
        icon={User}
        valueClassName="text-xl"
      />
      {/* Postal Address Card (Spans 2 columns) */}
      <SummaryCard
        title="Postal Address"
        value={client.postal_address || "No address provided"}
        className="md:col-span-2"
        valueClassName="text-sm font-normal whitespace-pre-line"
      />
      {client.contact_person && (
        <SummaryCard
          title="Contact Person"
          value={client.contact_person}
          className="md:col-span-2"
          valueClassName="text-sm font-normal"
        />
      )}
    </div>
  )
}
