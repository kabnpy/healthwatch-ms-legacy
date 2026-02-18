import React, { useMemo } from "react"
import type { MotorFinancialBreakdown } from "@/client"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LoadingButton } from "@/components/ui/loading-button"
import { useProducts, useQuoteQuery } from "@/hooks/useInsurance"
import type { EnhancedProduct, WizardState } from "@/types/insurance"

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
    return productsData?.data.find((p) => p.id === state.product_id) as
      | EnhancedProduct
      | undefined
  }, [state.product_id, productsData])

  const isMotorPrivate = selectedProduct?.class_of_insurance
    ?.toLowerCase()
    .includes("motor private")

  const quoteRequest = useMemo(() => {
    if (!state.product_id || !isMotorPrivate) return null
    return {
      product_id: state.product_id,
      risk_details: {
        "VEHICLE DETAILS": {
          "Value Kshs.": state.financials?.sumInsured || 0,
        },
        EXTENSIONS: {
          pvt: !!state.extensions?.pvt,
          excess_protector: !!state.extensions?.excessProtector,
          om_rescue_plus: !!state.extensions?.omRescuePlus,
        },
      },
    }
  }, [
    state.product_id,
    state.financials?.sumInsured,
    state.extensions,
    isMotorPrivate,
  ])

  const { data: quoteData } = useQuoteQuery(
    quoteRequest as any,
  )

  const breakdown =
    isMotorPrivate && quoteData
      ? (quoteData.breakdown as MotorFinancialBreakdown)
      : null

  const isPA = selectedProduct?.class_of_insurance
    ?.toLowerCase()
    .includes("personal accident")

  return (
    <div className="space-y-6">
      <div className="space-y-6">
        {/* Asset Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium uppercase text-muted-foreground tracking-wider">
              Product & Inputs
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Product:</span>
              <span className="font-bold">{selectedProduct?.name}</span>
            </div>
            <div className="border-t pt-2 mt-2 space-y-1">
              {(() => {
                const renderEntries = (
                  obj: any,
                  prefix = "",
                ): React.ReactNode => {
                  return Object.entries(obj || {}).map(([key, value]) => {
                    const label = prefix ? `${prefix} > ${key}` : key
                    if (
                      typeof value === "object" &&
                      value !== null &&
                      !Array.isArray(value)
                    ) {
                      return (
                        <React.Fragment key={label}>
                          {renderEntries(value, label)}
                        </React.Fragment>
                      )
                    }
                    return (
                      <div key={label} className="flex justify-between text-xs">
                        <span className="text-muted-foreground font-medium">
                          {label.replace(/_/g, " ")}:
                        </span>
                        <span className="font-mono">{String(value)}</span>
                      </div>
                    )
                  })
                }
                const entries = renderEntries(state.details)
                return Object.keys(state.details || {}).length === 0 ? (
                  <p className="text-xs text-muted-foreground italic">
                    No manual inputs required.
                  </p>
                ) : (
                  entries
                )
              })()}
            </div>
          </CardContent>
        </Card>

        {/* Financial Summary */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm font-medium uppercase text-muted-foreground tracking-wider flex justify-between">
              <span>Financial Summary</span>
              {breakdown && (
                <span className="text-[10px] font-bold text-emerald-600 border border-emerald-600 px-1 rounded">
                  AUTHORITATIVE
                </span>
              )}
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {!isPA && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Sum Insured:</span>
                <span className="font-bold">
                  KES {(state.financials?.sumInsured || 0).toLocaleString()}
                </span>
              </div>
            )}

            {breakdown ? (
              <div className="space-y-2 border-y py-3 my-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Net Premium:</span>
                  <span className="font-mono">
                    {Number(breakdown.net_premium).toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                    })}
                  </span>
                </div>
                {breakdown.benefits.map((benefit) => (
                  <div
                    key={benefit.name}
                    className="flex justify-between text-xs pl-4 italic"
                  >
                    <span className="text-muted-foreground">
                      {benefit.name}:
                    </span>
                    <span className="font-mono text-slate-600">
                      {Number(benefit.amount).toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                      })}
                    </span>
                  </div>
                ))}
                {Object.entries(breakdown.taxes).map(([name, amount]) => (
                  <div key={name} className="flex justify-between text-xs">
                    <span className="text-muted-foreground">
                      {name.replace(/_/g, " ").toUpperCase()}:
                    </span>
                    <span className="font-mono text-slate-600">
                      {Number(amount).toLocaleString(undefined, {
                        minimumFractionDigits: 2,
                      })}
                    </span>
                  </div>
                ))}
              </div>
            ) : null}

            <div className="flex justify-between pt-1">
              <span className="text-muted-foreground">Total Payable:</span>
              <span className="font-bold text-lg text-green-700">
                KES{" "}
                {(breakdown
                  ? Number(breakdown.total_amount)
                  : 0
                ).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </span>
            </div>
            <div className="flex justify-between border-t pt-2 text-sm">
              <span className="text-muted-foreground">Start Date:</span>
              <span className="font-medium">{state.financials?.startDate}</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="bg-blue-50 border border-blue-200 p-4 rounded-md text-sm text-blue-800">
        Review the captured inputs. The final Risk Note will be generated by
        combining these with the product's standard benefits and clauses.
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
          className="bg-blue-700 hover:bg-blue-800 h-10 px-8 font-bold"
        >
          Issue Policy
        </LoadingButton>
      </div>
    </div>
  )
}
