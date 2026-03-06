import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { RefreshCw } from "lucide-react"
import { Suspense } from "react"

import { PoliciesService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { EmptyState } from "@/components/Common/EmptyState"
import PendingItems from "@/components/Pending/PendingItems"
import { columns } from "@/components/Policies/columns"

function getRenewalsQueryOptions() {
  return {
    queryFn: () =>
      PoliciesService.readPolicies({ expiringWithin: 30, skip: 0, limit: 100 }),
    queryKey: ["renewals"],
  }
}

export const Route = createFileRoute("/_layout/renewals/")({
  component: Renewals,
  head: () => ({
    meta: [
      {
        title: "Renewals - HealthWatch MS",
      },
    ],
  }),
})

function RenewalsTableContent() {
  const { data: renewals } = useSuspenseQuery(getRenewalsQueryOptions())

  if (renewals.data.length === 0) {
    return (
      <EmptyState
        title="No renewals due"
        description="There are no policies expiring within the next 30 days."
        icon={RefreshCw}
      />
    )
  }

  return <DataTable columns={columns} data={renewals.data} />
}

function RenewalsTable() {
  return (
    <Suspense fallback={<PendingItems />}>
      <RenewalsTableContent />
    </Suspense>
  )
}

function Renewals() {
  return (
    <div className="flex flex-col gap-8">
      <div className="flex items-center justify-between border-b pb-6">
        <div>
          <h1 className="text-4xl font-bold tracking-tight">Renewals</h1>
          <p className="text-sm text-muted-foreground font-medium uppercase tracking-wider">
            Expiring Policies (Next 30 Days)
          </p>
        </div>
      </div>
      <RenewalsTable />
    </div>
  )
}
