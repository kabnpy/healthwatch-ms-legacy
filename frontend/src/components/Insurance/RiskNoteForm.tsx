import { zodResolver } from "@hookform/resolvers/zod"
import { useEffect } from "react"
import { useForm, type SubmitHandler } from "react-hook-form"
import { z } from "zod"

import type { ApiError, RiskNoteCreate } from "@/client"
import { Button } from "@/components/ui/button"
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
import { useCreateRiskNote } from "@/hooks/useInsurance"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

const formSchema = z.object({
  policy_id: z.string().uuid(),
  risk_note_number: z.string().min(1, "Required"),
  transaction_type: z.string(),
  start_date: z.string(),
  end_date: z.string(),
  sum_insured: z.coerce.number().min(0),
  basic_premium: z.coerce.number().min(0),
  training_levy: z.coerce.number().min(0),
  phcf_levy: z.coerce.number().min(0),
  stamp_duty: z.coerce.number().min(0),
  gross_premium: z.coerce.number().min(0),
  commission_amount: z.coerce.number().min(0),
})

interface FormData {
  policy_id: string
  risk_note_number: string
  transaction_type: string
  start_date: string
  end_date: string
  sum_insured: number
  basic_premium: number
  training_levy: number
  phcf_levy: number
  stamp_duty: number
  gross_premium: number
  commission_amount: number
}

interface RiskNoteFormProps {
  policyId: string
  onSuccess?: () => void
  onCancel?: () => void
}

export const RiskNoteForm = ({ policyId, onSuccess, onCancel }: RiskNoteFormProps) => {
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const createRiskNote = useCreateRiskNote()

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema) as any,
    defaultValues: {
      policy_id: policyId,
      risk_note_number: `RN-${Math.floor(Math.random() * 100000)}`,
      transaction_type: "New Business",
      start_date: new Date().toISOString().split("T")[0],
      end_date: new Date(new Date().setFullYear(new Date().getFullYear() + 1)).toISOString().split("T")[0],
      sum_insured: 0,
      basic_premium: 0,
      training_levy: 0,
      phcf_levy: 0,
      stamp_duty: 40,
      gross_premium: 0,
      commission_amount: 0,
    },
  })

  const sumInsured = form.watch("sum_insured")

  useEffect(() => {
    if (sumInsured > 0) {
      const basic = sumInsured * 0.04
      const training = basic * 0.002
      const phcf = basic * 0.0025
      const stamp = 40
      const gross = basic + training + phcf + stamp
      const commission = basic * 0.125 // 12.5% default

      form.setValue("basic_premium", basic)
      form.setValue("training_levy", parseFloat(training.toFixed(2)))
      form.setValue("phcf_levy", parseFloat(phcf.toFixed(2)))
      form.setValue("gross_premium", parseFloat(gross.toFixed(2)))
      form.setValue("commission_amount", parseFloat(commission.toFixed(2)))
    }
  }, [sumInsured, form])

  const onSubmit: SubmitHandler<FormData> = (data) => {
    const { sum_insured, ...rest } = data
    const riskNoteData: RiskNoteCreate = rest
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
        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control}
            name="risk_note_number"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Risk Note #</FormLabel>
                <FormControl>
                  <Input {...field} readOnly />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
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

        <div className="grid grid-cols-2 gap-4">
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

        <div className="bg-muted/30 p-4 rounded-lg space-y-2">
          <div className="flex justify-between text-sm">
            <span>Basic Premium (4%):</span>
            <span className="font-mono">{form.watch("basic_premium").toLocaleString()}</span>
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Training Levy (0.2%):</span>
            <span>{form.watch("training_levy")}</span>
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>PHCF Levy (0.25%):</span>
            <span>{form.watch("phcf_levy")}</span>
          </div>
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>Stamp Duty:</span>
            <span>40.00</span>
          </div>
          <div className="flex justify-between font-bold border-t pt-2 mt-2">
            <span>GROSS PREMIUM:</span>
            <span>{form.watch("gross_premium").toLocaleString()}</span>
          </div>
        </div>

        <div className="flex justify-end gap-4 pt-4">
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <LoadingButton type="submit" loading={createRiskNote.isPending}>
            Create Risk Note
          </LoadingButton>
        </div>
      </form>
    </Form>
  )
}