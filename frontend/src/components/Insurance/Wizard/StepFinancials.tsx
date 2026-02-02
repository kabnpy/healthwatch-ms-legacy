import { zodResolver } from "@hookform/resolvers/zod"
import { useMemo } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useProducts } from "@/hooks/useInsurance"
import { calculatePremium } from "@/lib/calculator"

const financialsSchema = z.object({
  financials: z.object({
    sumInsured: z.coerce.number().min(0),
    rate: z.coerce.number().min(0),
    startDate: z.string(),
    duration: z.coerce.number().default(12),
  }),
  extensions: z.object({
    pvt: z.boolean().default(false),
    excessProtector: z.boolean().default(false),
    passengerLiability: z.boolean().default(false),
  }),
})

interface StepFinancialsProps {
  defaultValues: any
  onNext: (data: any) => void
  onBack: () => void
  productId: string
}

export function StepFinancials({
  defaultValues,
  onNext,
  onBack,
  productId,
}: StepFinancialsProps) {
  const { data: productsData } = useProducts()

  const selectedProduct = useMemo(() => {
    return productsData?.data.find((p) => p.id === productId)
  }, [productId, productsData])

  const form = useForm({
    resolver: zodResolver(financialsSchema),
    defaultValues,
  })

  const watchedValues = form.watch()
  const calculation = calculatePremium({
    sumInsured: watchedValues.financials.sumInsured || 0,
    rate: watchedValues.financials.rate || 0,
    hasPVT: watchedValues.extensions.pvt,
    hasExcessProtector: watchedValues.extensions.excessProtector,
    hasPassengerLiability: watchedValues.extensions.passengerLiability,
  })

  const isPA = selectedProduct?.class_of_insurance
    ?.toLowerCase()
    .includes("personal accident")
  const isMotor = selectedProduct?.class_of_insurance
    ?.toLowerCase()
    .includes("motor")

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onNext)} className="space-y-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Inputs */}
          <div className="lg:col-span-2 space-y-6">
            <div className="grid grid-cols-2 gap-4">
              {!isPA && (
                <FormField
                  control={form.control}
                  name="financials.sumInsured"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Sum Insured</FormLabel>
                      <FormControl>
                        <Input type="number" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}
              <FormField
                control={form.control}
                name="financials.rate"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      {isPA ? "Premium (Flat Amount)" : "Rate (%)"}
                    </FormLabel>
                    <FormControl>
                      <Input type="number" step="0.01" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <FormField
                control={form.control}
                name="financials.startDate"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Start Date</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="financials.duration"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Duration (Months)</FormLabel>
                    <FormControl>
                      <Input type="number" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            {isMotor && (
              <div className="space-y-4">
                <h3 className="text-sm font-semibold uppercase text-muted-foreground">
                  Motor Extensions
                </h3>
                <div className="grid grid-cols-1 gap-4 border rounded-md p-4 bg-muted/10">
                  <FormField
                    control={form.control}
                    name="extensions.pvt"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between space-y-0 rounded-lg p-2 border">
                        <FormLabel className="text-base cursor-pointer">
                          Political Violence & Terrorism (0.25%)
                        </FormLabel>
                        <FormControl>
                          <Checkbox
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="extensions.excessProtector"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between space-y-0 rounded-lg p-2 border">
                        <FormLabel className="text-base cursor-pointer">
                          Excess Protector (0.25%)
                        </FormLabel>
                        <FormControl>
                          <Checkbox
                            checked={field.value}
                            onCheckedChange={field.onChange}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                </div>
              </div>
            )}
          </div>

          {/* Preview */}
          <div className="lg:col-span-1">
            <div className="sticky top-0 bg-muted/30 border rounded-lg p-6 space-y-4">
              <h3 className="font-bold text-center border-b pb-2">
                PREMIUM PREVIEW
              </h3>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between font-bold">
                  <span>{isPA ? "Base Premium:" : "Basic Premium:"}</span>
                  <span className="font-mono">
                    {calculation.breakdown.basic.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                    })}
                  </span>
                </div>

                {isMotor &&
                  calculation.breakdown.extensions.map((ext) => (
                    <div
                      key={ext.name}
                      className="flex justify-between text-blue-600"
                    >
                      <span>+ {ext.name}:</span>
                      <span>
                        {ext.amount.toLocaleString(undefined, {
                          minimumFractionDigits: 2,
                        })}
                      </span>
                    </div>
                  ))}

                <div className="border-t pt-2 mt-2">
                  <div className="flex justify-between text-muted-foreground">
                    <span>Training Levy:</span>
                    <span>
                      {calculation.breakdown.levies.trainingLevy.toLocaleString(
                        undefined,
                        { minimumFractionDigits: 2 },
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between text-muted-foreground">
                    <span>PHCF Levy:</span>
                    <span>
                      {calculation.breakdown.levies.phcf.toLocaleString(
                        undefined,
                        { minimumFractionDigits: 2 },
                      )}
                    </span>
                  </div>
                </div>
              </div>

              <div className="border-t-2 border-black pt-4 mt-4">
                <div className="flex justify-between items-center">
                  <span className="font-bold">TOTAL:</span>
                  <span className="text-xl font-bold text-green-700 font-mono">
                    KES{" "}
                    {calculation.breakdown.total.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                    })}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-between pt-4 border-t">
          <Button type="button" variant="outline" onClick={onBack}>
            Back: Asset Details
          </Button>
          <Button type="submit">Next: Review & Issue</Button>
        </div>
      </form>
    </Form>
  )
}
