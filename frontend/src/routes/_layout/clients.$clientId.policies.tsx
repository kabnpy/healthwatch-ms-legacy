import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Plus, Users } from "lucide-react"
import { useState } from "react"
import { PoliciesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { NewPolicyWizard } from "@/components/Insurance/Wizard/NewPolicyWizard"
import { columns as policyColumns } from "@/components/Policies/columns"
import { Button } from "@/components/ui/button"

function getPoliciesQueryOptions(clientId: string) {
  return {
    queryFn: () =>
      PoliciesService.readPolicies({ clientId, skip: 0, limit: 100 }),
    queryKey: ["policies", { clientId }],
  }
}

export const Route = createFileRoute("/_layout/clients/$clientId/policies")({
  component: ClientPolicies,
})

function ClientPolicies() {
  const { clientId } = Route.useParams()
  const { data: policies } = useSuspenseQuery(getPoliciesQueryOptions(clientId))
  const [wizardOpen, setWizardOpen] = useState(false)

  return (
    <div className="space-y-4 pt-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold tracking-tight">Policies</h2>
        <Button onClick={() => setWizardOpen(true)} className="gap-2">
          <Plus className="size-4" />
          New Policy
        </Button>
      </div>
      {policies.data.length === 0 ? (
        <div className="flex flex-col items-center justify-center text-center py-12 border rounded-lg bg-muted/5">
          <div className="rounded-full bg-muted p-4 mb-4">
            <Users className="h-8 w-8 text-muted-foreground" />
          </div>
          <h3 className="text-lg font-semibold">No policies found</h3>
          <p className="text-muted-foreground">
            Create a new policy using the wizard
          </p>
        </div>
      ) : (
        <DataTable columns={policyColumns} data={policies.data} />
      )}

      <NewPolicyWizard
        clientId={clientId}
        isOpen={wizardOpen}
        onClose={() => setWizardOpen(false)}
      />
    </div>
  )
}
