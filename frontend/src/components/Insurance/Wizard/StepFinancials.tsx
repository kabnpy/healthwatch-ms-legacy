import { zodResolver } from "@hookform/resolvers/zod"
import { useEffect, useMemo } from "react"
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
import type {
  EnhancedProduct,
  WizardExtensions,
  WizardFinancials,
} from "@/types/insurance"

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
    omRescuePlus: z.boolean().default(false),
  }),
})

interface StepFinancialsProps {
  defaultValues: {
    financials: WizardFinancials
    extensions: WizardExtensions
  }
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
    return productsData?.data.find((p) => p.id === productId) as
      | EnhancedProduct
      | undefined
  }, [productId, productsData])

  const form = useForm({
    resolver: zodResolver(financialsSchema),
    defaultValues: {
      financials: {
        sumInsured: defaultValues.financials?.sumInsured || 0,
        rate: defaultValues.financials?.rate || 0,
        startDate:
          defaultValues.financials?.startDate ||
          new Date().toISOString().split("T")[0],
        duration: defaultValues.financials?.duration || 12,
      },
      extensions: {
        pvt: defaultValues.extensions?.pvt || false,
        excessProtector: defaultValues.extensions?.excessProtector || false,
        passengerLiability:
          defaultValues.extensions?.passengerLiability || false,
        omRescuePlus: defaultValues.extensions?.omRescuePlus || false,
      },
    },
  })

  const watchedValues = form.watch() as any
  const financials = watchedValues.financials || {}
  const extensions = watchedValues.extensions || {}

  const isPA = selectedProduct?.class_of_insurance
    ?.toLowerCase()
    .includes("personal accident")

  const isMotor = selectedProduct?.class_of_insurance
    ?.toLowerCase()
    .includes("motor")

  const isMotorPrivate = selectedProduct?.class_of_insurance
    ?.toLowerCase()
    .includes("motor private")

  const calculation = calculatePremium({
    sumInsured: financials.sumInsured || 0,
    rate: financials.rate || 0,
    hasPVT: !!extensions.pvt,
    hasExcessProtector: !!extensions.excessProtector,
    hasPassengerLiability: !!extensions.passengerLiability,
    hasOMRescuePlus: !!extensions.omRescuePlus,
    isMotorPrivate: !!isMotorPrivate,
  })

  // Auto-set rate for Motor Private
  useEffect(() => {
    if (isMotorPrivate && calculation.breakdown.basic > 0) {
      // Reverse calculate effective rate for display
      const effectiveRate =
        (calculation.breakdown.basic / (financials.sumInsured || 1)) * 100
      if (effectiveRate !== financials.rate) {
        form.setValue("financials.rate", Number(effectiveRate.toFixed(3)))
      }
    }
  }, [
    isMotorPrivate,
    calculation.breakdown.basic,
    financials.sumInsured,
    financials.rate,
    form.setValue,
  ])

  // High-End Logic: Auto-select included benefits
  useEffect(() => {
    if (isMotorPrivate && (financials.sumInsured || 0) >= 3000000) {
      if (!extensions.pvt) form.setValue("extensions.pvt", true)
      if (!extensions.excessProtector)
        form.setValue("extensions.excessProtector", true)
    }
  }, [
    isMotorPrivate,
    financials.sumInsured,
    extensions.excessProtector,
    extensions.pvt,
    form.setValue,
  ])

  const isHighEnd = isMotorPrivate && (financials.sumInsured || 0) >= 3000000

  return (
    <Form {...(form as any)}>
      <form onSubmit={form.handleSubmit(onNext)} className="space-y-6">
        <div className="space-y-8">
          {/* Inputs Section */}
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {!isPA && (
                <FormField
                  control={form.control as any}
                  name="financials.sumInsured"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Sum Insured</FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          value={field.value || 0}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              )}
              <FormField
                control={form.control as any}
                name="financials.rate"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>
                      {isPA ? "Premium (Flat Amount)" : "Rate (%)"}
                    </FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        step="0.01"
                        {...field}
                        value={field.value || 0}
                        readOnly={!!isMotorPrivate}
                        className={isMotorPrivate ? "bg-slate-100" : ""}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <FormField
                control={form.control as any}
                name="financials.startDate"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Start Date</FormLabel>
                    <FormControl>
                      <Input type="date" {...field} value={field.value || ""} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control as any}
                name="financials.duration"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Duration (Months)</FormLabel>
                    <FormControl>
                      <Input
                        type="number"
                        {...field}
                        value={field.value || 12}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            {isMotor && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-sm font-semibold uppercase text-muted-foreground tracking-wider">
                    Benefits (Extensions)
                  </h3>
                  {isHighEnd && (
                    <span className="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold uppercase tracking-wider">
                      High-End: All Inclusive
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 border rounded-md p-4 bg-muted/10">
                  <FormField
                    control={form.control as any}
                    name="extensions.pvt"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between space-y-0 rounded-lg p-2 border bg-white">
                        <FormLabel className="text-sm cursor-pointer w-full">
                          Political Violence & Terrorism (0.25%)
                          {isHighEnd && (
                            <span className="ml-2 text-[10px] font-bold text-emerald-600 block">
                              (INCLUDED)
                            </span>
                          )}
                        </FormLabel>
                        <FormControl>
                          <Checkbox
                            checked={!!field.value}
                            onCheckedChange={field.onChange}
                            disabled={isHighEnd}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control as any}
                    name="extensions.excessProtector"
                    render={({ field }) => (
                      <FormItem className="flex items-center justify-between space-y-0 rounded-lg p-2 border bg-white">
                        <FormLabel className="text-sm cursor-pointer w-full">
                          Excess Protector (0.25%)
                          {isHighEnd && (
                            <span className="ml-2 text-[10px] font-bold text-emerald-600 block">
                              (INCLUDED)
                            </span>
                          )}
                        </FormLabel>
                        <FormControl>
                          <Checkbox
                            checked={!!field.value}
                            onCheckedChange={field.onChange}
                            disabled={isHighEnd}
                          />
                        </FormControl>
                      </FormItem>
                    )}
                  />
                  {isMotorPrivate && (
                    <FormField
                      control={form.control as any}
                      name="extensions.omRescuePlus"
                      render={({ field }) => (
                        <FormItem className="flex items-center justify-between space-y-0 rounded-lg p-2 border bg-white">
                          <FormLabel className="text-sm cursor-pointer w-full">
                            OM Rescue Plus (KES 1,000)
                          </FormLabel>
                          <FormControl>
                            <Checkbox
                              checked={!!field.value}
                              onCheckedChange={field.onChange}
                            />
                          </FormControl>
                        </FormItem>
                      )}
                    />
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Preview Section */}
          <div className="bg-slate-900 text-white rounded-lg p-6 shadow-xl border border-slate-800">
            <div className="flex items-center justify-between border-b border-slate-700 pb-4 mb-4">
              <h3 className="font-bold text-sm uppercase tracking-widest text-slate-400">
                Premium Preview
              </h3>
              <div className="text-right text-[10px] font-mono text-slate-500">
                Calculated Real-time
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-3">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-slate-400">
                    {isPA ? "Base Premium" : "Basic Premium"}
                  </span>
                  <span className="font-mono font-bold">
                    {calculation.breakdown.basic.toLocaleString(undefined, {
                      minimumFractionDigits: 2,
                    })}
                  </span>
                </div>

                <div className="space-y-1">
                  <span className="text-[10px] font-bold uppercase text-slate-500 tracking-tight">
                    Benefits
                  </span>
                  {isMotor && calculation.breakdown.extensions.length > 0 ? (
                    calculation.breakdown.extensions.map((ext) => (
                      <div
                        key={ext.name}
                        className="flex justify-between text-xs py-1 border-b border-slate-800 last:border-0"
                      >
                        <span className="text-slate-300 italic">
                          {ext.name}
                        </span>
                        <span
                          className={
                            ext.included
                              ? "font-bold text-emerald-400"
                              : "font-mono"
                          }
                        >
                          {ext.included
                            ? "INCLUDED"
                            : ext.amount.toLocaleString(undefined, {
                                minimumFractionDigits: 2,
                              })}
                        </span>
                      </div>
                    ))
                  ) : (
                    <p className="text-[10px] text-slate-600 italic">
                      No additional benefits selected.
                    </p>
                  )}
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-slate-800/50 p-3 rounded space-y-2">
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">Training Levy (0.2%)</span>
                    <span className="font-mono text-slate-300">
                      {calculation.breakdown.levies.trainingLevy.toLocaleString(
                        undefined,
                        { minimumFractionDigits: 2 },
                      )}
                    </span>
                  </div>
                  <div className="flex justify-between text-xs">
                    <span className="text-slate-400">PHCF Levy (0.25%)</span>
                    <span className="font-mono text-slate-300">
                      {calculation.breakdown.levies.phcf.toLocaleString(
                        undefined,
                        { minimumFractionDigits: 2 },
                      )}
                    </span>
                  </div>
                </div>

                <div className="pt-2 border-t border-slate-700">
                  <div className="flex justify-between items-baseline">
                    <span className="text-xs font-bold text-slate-400 uppercase">
                      Total Amount
                    </span>
                    <div className="text-right">
                      <span className="text-2xl font-black text-emerald-400 font-mono">
                        <span className="text-sm font-normal mr-1">KES</span>
                        {calculation.breakdown.total.toLocaleString(undefined, {
                          minimumFractionDigits: 2,
                        })}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="flex justify-between pt-6 border-t mt-4">
          <Button type="button" variant="outline" onClick={onBack}>
            Back: Asset Details
          </Button>
          <Button type="submit" size="lg" className="px-8">
            Next: Review & Issue
          </Button>
        </div>
      </form>
    </Form>
  )
}
