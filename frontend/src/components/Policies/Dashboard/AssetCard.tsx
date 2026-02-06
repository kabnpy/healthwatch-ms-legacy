import { Car } from "lucide-react"
import type { PolicyPublic } from "@/client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

interface AssetCardProps {
  policy?: PolicyPublic
}

export function AssetCard({ policy }: AssetCardProps) {
  if (!policy) {
    return (
      <Card className="h-full border-dashed bg-muted/40">
        <CardContent className="flex flex-col items-center justify-center h-full py-12 text-muted-foreground">
          <Car className="size-12 mb-4 opacity-50" />
          <p>No Policy Data Found</p>
        </CardContent>
      </Card>
    )
  }

  // Assuming details is a generic dict
  const details = (policy.risk_details as Record<string, any>) || {}

  return (
    <Card className="h-full shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
          Insured Asset
        </CardTitle>
        <Car className="size-4 text-blue-600" />
      </CardHeader>
      <CardContent>
        <div className="flex flex-col gap-4">
          <div>
            <div className="text-xl font-bold truncate">{policy.description}</div>
            <p className="text-sm text-muted-foreground">
              {policy.product?.class_of_insurance || "Insurance"} cover
            </p>
          </div>

          <div className="space-y-2 text-sm">
            <div className="flex justify-between border-b pb-1">
              <span className="text-muted-foreground">Insured Value</span>
              <span className="font-mono font-semibold">
                KES {(details.sum_insured || 0).toLocaleString()}
              </span>
            </div>
            {Object.entries(details)
              .slice(0, 3)
              .map(([key, value]) => (
                <div
                  key={key}
                  className="flex justify-between border-b pb-1 last:border-0"
                >
                  <span className="text-muted-foreground capitalize">
                    {key.replace(/_/g, " ")}
                  </span>
                  <span className="font-medium text-right truncate max-w-[150px]">
                    {String(value)}
                  </span>
                </div>
              ))}
          </div>
        </div>
      </CardContent>
    </Card>
  )
}