import { zodResolver } from "@hookform/resolvers/zod"
import { type SubmitHandler, useForm } from "react-hook-form"
import { z } from "zod"

import type { ApiError, RiskNoteCreate } from "@/client"
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
import { LoadingButton } from "@/components/ui/loading-button"
import useCustomToast from "@/hooks/useCustomToast"
import { useCreateRiskNote } from "@/hooks/useInsurance"
import { calculatePremium } from "@/lib/calculator"
import { handleError } from "@/utils"

const formSchema = z.object({
  policy_id: z.string().uuid(),
  transaction_type: z.string(),
  start_date: z.string(),
  end_date: z.string(),
  sum_insured: z.coerce.number().min(0),
  rate: z.coerce.number().min(0).default(4),
  hasPVT: z.boolean().default(false),
  hasExcessProtector: z.boolean().default(false),
  commission_rate: z.coerce.number().min(0).default(12.5),
})

interface FormData {
  policy_id: string
  transaction_type: string
  start_date: string
  end_date: string
  sum_insured: number
  rate: number
  hasPVT: boolean
  hasExcessProtector: boolean
  commission_rate: number
}

interface RiskNoteFormProps {
  policyId: string
  initialTransactionType?: string
  onSuccess?: () => void
  onCancel?: () => void
}

export const RiskNoteForm = ({
  policyId,
  initialTransactionType = "New Business",
  onSuccess,
  onCancel,
}: RiskNoteFormProps) => {
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const createRiskNote = useCreateRiskNote()

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema) as any,
    defaultValues: {
      policy_id: policyId,
      transaction_type: initialTransactionType,
      start_date: new Date().toISOString().split("T")[0],
      end_date: new Date(new Date().setFullYear(new Date().getFullYear() + 1))
        .toISOString()
        .split("T")[0],
      sum_insured: 0,
      rate: 4,
      hasPVT: false,
      hasExcessProtector: false,
      commission_rate: 12.5,
    },
  })

  // Watch fields for real-time calculation
  const sumInsured = form.watch("sum_insured")
  const rate = form.watch("rate")
  const hasPVT = form.watch("hasPVT")
  const hasExcessProtector = form.watch("hasExcessProtector")

  // Calculate premium on the fly
  const calculation = calculatePremium({
    sumInsured,
    rate,
    hasPVT,
    hasExcessProtector,
  })

  const { breakdown } = calculation

  const onSubmit: SubmitHandler<FormData> = (data) => {
    // 1. Prepare the payload
    const riskNoteData: RiskNoteCreate = {
      policy_id: data.policy_id,
      transaction_type: data.transaction_type,
      start_date: data.start_date,
      end_date: data.end_date,
      net_premium:
        breakdown.basic +
        breakdown.extensions.reduce((acc, curr) => acc + curr.amount, 0),
      taxes: breakdown.levies as any,
      commission_amount: breakdown.basic * (data.commission_rate / 100),
      total_amount: breakdown.total,
      items_snapshot: {}, // Will be handled in wizard or dashboard
      special_clauses: [],
    }

    createRiskNote.mutate(riskNoteData, {
      onSuccess: () => {
        showSuccessToast("Risk Note created successfully")
        onSuccess?.()
      },
      onError: (err: Error) => {
        handleError.call(showErrorToast, err as ApiError)
      },
    })
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-1 gap-4">
          <FormField
            control={form.control}
            name="sum_insured"
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
        </div>

        <div className="grid grid-cols-3 gap-4">
          <FormField
            control={form.control}
            name="rate"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Rate (%)</FormLabel>
                <FormControl>
                  <Input type="number" step="0.01" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="start_date"
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
            name="end_date"
            render={({ field }) => (
              <FormItem>
                <FormLabel>End Date</FormLabel>
                <FormControl>
                  <Input type="date" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        {/* Extensions Toggles */}
        <div className="flex gap-6 p-4 border rounded-md bg-muted/20">
          <FormField
            control={form.control}
            name="hasPVT"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Include PVT (0.25%)</FormLabel>
                </div>
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="hasExcessProtector"
            render={({ field }) => (
              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                <FormControl>
                  <Checkbox
                    checked={field.value}
                    onCheckedChange={field.onChange}
                  />
                </FormControl>
                <div className="space-y-1 leading-none">
                  <FormLabel>Include Excess Protector (0.25%)</FormLabel>
                </div>
              </FormItem>
            )}
          />
        </div>

        {/* Live Calculation Preview */}
        <div className="bg-muted/50 p-4 rounded-lg space-y-2 border border-muted-foreground/20">
          <div className="flex justify-between text-sm">
            <span>Basic Premium ({rate}%):</span>
            <span className="font-mono">
              {breakdown.basic.toLocaleString(undefined, {
                minimumFractionDigits: 2,
              })}
            </span>
          </div>

          {breakdown.extensions.map((ext) => (
            <div
              key={ext.name}
              className="flex justify-between text-sm text-blue-600"
            >
              <span>+ {ext.name}:</span>
              <span>
                {ext.amount.toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                })}
              </span>
            </div>
          ))}

          <div className="border-t my-2 border-dashed" />

          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Training Levy (0.2%):</span>
            <span>
              {breakdown.levies.trainingLevy.toLocaleString(undefined, {
                minimumFractionDigits: 2,
              })}
            </span>
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>PHCF Levy (0.25%):</span>
            <span>
              {breakdown.levies.phcf.toLocaleString(undefined, {
                minimumFractionDigits: 2,
              })}
            </span>
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Stamp Duty:</span>
            <span>
              {breakdown.levies.stampDuty.toLocaleString(undefined, {
                minimumFractionDigits: 2,
              })}
            </span>
          </div>

          <div className="flex justify-between font-bold border-t border-black pt-2 mt-2 text-lg">
            <span>TOTAL PAYABLE:</span>
            <span>
              {breakdown.total.toLocaleString(undefined, {
                minimumFractionDigits: 2,
              })}
            </span>
          </div>
        </div>

        <div className="flex justify-end gap-4 pt-4">
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <LoadingButton type="submit" loading={createRiskNote.isPending}>
            Generate Risk Note
          </LoadingButton>
        </div>
      </form>
    </Form>
  )
}
