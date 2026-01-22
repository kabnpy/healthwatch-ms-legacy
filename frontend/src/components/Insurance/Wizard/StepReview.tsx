import { WizardState } from "@/types/wizard"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { calculatePremium } from "@/lib/calculator"
import { LoadingButton } from "@/components/ui/loading-button"

interface StepReviewProps {
  state: WizardState
  onIssue: () => void
  onBack: () => void
  isSubmitting?: boolean
}

export function StepReview({ state, onIssue, onBack, isSubmitting }: StepReviewProps) {
  const calculation = calculatePremium({
    sumInsured: state.financials.sumInsured,
    rate: state.financials.rate,
    hasPVT: state.extensions.pvt,
    hasExcessProtector: state.extensions.excessProtector,
    hasPassengerLiability: state.extensions.passengerLiability,
  })

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Asset Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium uppercase text-muted-foreground tracking-wider">Asset Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Registration:</span>
              <span className="font-bold">{state.asset.identifier}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Make & Model:</span>
              <span className="font-medium">{state.asset.makeModel}</span>
            </div>
            {state.asset.details.chassis && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Chassis:</span>
                <span className="text-xs font-mono uppercase">{state.asset.details.chassis}</span>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Financial Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium uppercase text-muted-foreground tracking-wider">Financial Summary</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Sum Insured:</span>
              <span className="font-bold">KES {state.financials.sumInsured.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Total Premium:</span>
              <span className="font-bold text-green-700">KES {calculation.breakdown.total.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Start Date:</span>
              <span className="font-medium">{state.financials.startDate}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-md text-sm text-yellow-800">
        Please verify all details before issuing the policy. This action will generate an official tax invoice and a certificate of insurance.
      </div>

      <div className="flex justify-between pt-4 border-t">
        <Button type="button" variant="outline" onClick={onBack} disabled={isSubmitting}>Back: Financials</Button>
        <LoadingButton 
            onClick={onIssue} 
            loading={isSubmitting}
            className="bg-green-700 hover:bg-green-800"
        >
            Issue Policy & Generate Documents
        </LoadingButton>
      </div>
    </div>
  )
}
