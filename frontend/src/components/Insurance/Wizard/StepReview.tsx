import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LoadingButton } from "@/components/ui/loading-button"
import { calculatePremium } from "@/lib/calculator"
import type { WizardState } from "@/types/wizard"
import { useProducts } from "@/hooks/useInsurance"
import { useMemo } from "react"

interface StepReviewProps {
  state: WizardState
  onIssue: () => void
  onBack: () => void
  isSubmitting?: boolean
}

export function StepReview({
  state,
  onIssue,
  onBack,
  isSubmitting,
}: StepReviewProps) {
  const { data: productsData } = useProducts()
  
  const selectedProduct = useMemo(() => {
    return productsData?.data.find((p) => p.id === state.product_id)
  }, [state.product_id, productsData])

  const calculation = calculatePremium({
    sumInsured: state.financials.sumInsured,
    rate: state.financials.rate,
    hasPVT: state.extensions.pvt,
    hasExcessProtector: state.extensions.excessProtector,
    hasPassengerLiability: state.extensions.passengerLiability,
  })

  const isPA = selectedProduct?.class_of_insurance?.toLowerCase().includes("personal accident")

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Asset Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium uppercase text-muted-foreground tracking-wider">
              Asset/Risk Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Product:</span>
              <span className="font-bold">{selectedProduct?.name}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Description:</span>
              <span className="font-medium">{state.asset.description}</span>
            </div>
            <div className="border-t pt-2 mt-2 space-y-1">
               {Object.entries(state.asset.details || {}).map(([key, value]) => (
                 <div key={key} className="flex justify-between text-xs">
                   <span className="text-muted-foreground capitalize">{key.replace(/_/g, ' ')}:</span>
                   <span className="font-mono">{String(value)}</span>
                 </div>
               ))}
            </div>
          </CardContent>
        </Card>

        {/* Financial Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium uppercase text-muted-foreground tracking-wider">
              Financial Summary
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {!isPA && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Sum Insured:</span>
                <span className="font-bold">
                  KES {state.financials.sumInsured.toLocaleString()}
                </span>
              </div>
            )}
            <div className="flex justify-between">
              <span className="text-muted-foreground">Total Premium:</span>
              <span className="font-bold text-green-700">
                KES{" "}
                {calculation.breakdown.total.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </span>
            </div>
            <div className="flex justify-between border-t pt-2">
              <span className="text-muted-foreground">Period:</span>
              <span className="font-medium">
                {state.financials.startDate} (12 Months)
              </span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="bg-blue-50 border border-blue-200 p-4 rounded-md text-sm text-blue-800">
        Review all details above. Issuing this policy will create the final Risk Note and initiate the debit note for the client.
      </div>

      <div className="flex justify-between pt-4 border-t">
        <Button
          type="button"
          variant="outline"
          onClick={onBack}
          disabled={isSubmitting}
        >
          Back: Financials
        </Button>
        <LoadingButton
          onClick={onIssue}
          loading={isSubmitting}
          className="bg-blue-700 hover:bg-blue-800"
        >
          Confirm & Issue Policy
        </LoadingButton>
      </div>
    </div>
  )
}