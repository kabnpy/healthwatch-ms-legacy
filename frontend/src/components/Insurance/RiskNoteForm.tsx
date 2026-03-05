import { zodResolver } from "@hookform/resolvers/zod"
import { useEffect } from "react"
import { type SubmitHandler, useForm } from "react-hook-form"
import { z } from "zod"
import type { ApiError, RiskNoteStatus } from "@/client"
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import useCustomToast from "@/hooks/useCustomToast"
import {
  useCreateRiskNote,
  usePolicy,
  useRiskNote,
  useUpdateRiskNote,
} from "@/hooks/useInsurance"
import { handleError } from "@/utils"

interface RiskNoteFormProps {
  policyId: string
  riskNoteId?: string // If provided, we are editing an existing (likely draft) risk note
  initialStatus?: string
  initialTransactionType?: string
  onSuccess?: () => void
  onCancel?: () => void
}

export const RiskNoteForm = ({
  policyId,
  riskNoteId,
  initialStatus,
  initialTransactionType,
  onSuccess,
  onCancel,
}: RiskNoteFormProps) => {
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const { data: policy, isLoading: isLoadingPolicy } = usePolicy(policyId)
  const { data: existingRiskNote, isLoading: isLoadingRiskNote } = useRiskNote(
    riskNoteId || "",
  )
  const updateRiskNote = useUpdateRiskNote()
  const createRiskNote = useCreateRiskNote()

  const formSchema = z.object({
    transaction_type: z.string().min(1),
    coverage_start: z.string().min(1),
    coverage_end: z.string().min(1),
    status: z.string().min(1),
    net_premium: z.coerce.number().min(0),
    commission_amount: z.coerce.number().min(0),
    details: z.record(z.string(), z.any()), // Dynamic fields from form_schema
  })

  type FormData = z.infer<typeof formSchema>

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema) as any,
    defaultValues: {
      transaction_type: initialTransactionType || "New Business",
      coverage_start: new Date().toISOString().split("T")[0],
      coverage_end: new Date(
        new Date().setFullYear(new Date().getFullYear() + 1),
      )
        .toISOString()
        .split("T")[0],
      status: initialStatus || "Draft",
      net_premium: 0,
      commission_amount: 0,
      details: {},
    },
  })

  // Populate form when data is loaded
  useEffect(() => {
    if (existingRiskNote) {
      const coverSnapshot = existingRiskNote.cover_snapshot || {}
      const existingRN = existingRiskNote as any

      form.reset({
        transaction_type: existingRiskNote.transaction_type,
        coverage_start:
          existingRiskNote.coverage_start ||
          (existingRiskNote as any).start_date,
        coverage_end:
          existingRiskNote.coverage_end || (existingRiskNote as any).end_date,
        status: existingRN.status || "Draft",
        net_premium: Number(existingRiskNote.net_premium),
        commission_amount: Number(existingRiskNote.commission_amount),
        details: coverSnapshot,
      })
    } else if (policy) {
      const activeNote = (policy as any).active_note
      form.reset({
        transaction_type: initialTransactionType || "New Business",
        coverage_start:
          activeNote?.coverage_start || new Date().toISOString().split("T")[0],
        coverage_end:
          activeNote?.coverage_end ||
          new Date(new Date().setFullYear(new Date().getFullYear() + 1))
            .toISOString()
            .split("T")[0],
        status: initialStatus || "Draft",
        net_premium: Number(activeNote?.net_premium || 0),
        commission_amount: Number(activeNote?.commission_amount || 0),
        details: activeNote?.cover_snapshot || {},
      })
    }
  }, [existingRiskNote, policy, form, initialStatus, initialTransactionType])

  const onSubmit: SubmitHandler<FormData> = (data) => {
    // Basic tax calculation for now (matching seeding logic)
    const trainingLevy = data.net_premium * 0.002
    const phcf = data.net_premium * 0.0025
    const total_amount = data.net_premium + trainingLevy + phcf

    const payload = {
      policy_id: policyId,
      transaction_type: data.transaction_type,
      coverage_start: data.coverage_start,
      coverage_end: data.coverage_end,
      net_premium: data.net_premium,
      commission_amount: data.commission_amount,
      status: data.status as RiskNoteStatus,
      cover_snapshot: data.details,
      financial_breakdown: {
        taxes: { training_levy: trainingLevy, phcf: phcf },
        net_premium: data.net_premium,
        total_amount,
        commission_amount: data.commission_amount,
      },
      total_amount,
    }

    if (riskNoteId) {
      updateRiskNote.mutate(
        { id: riskNoteId, data: payload as any },
        {
          onSuccess: () => {
            showSuccessToast("Risk Note Updated")
            onSuccess?.()
          },
          onError: (err: Error) => {
            handleError.call(showErrorToast, err as ApiError)
          },
        },
      )
    } else {
      createRiskNote.mutate(payload as any, {
        onSuccess: () => {
          showSuccessToast("New Risk Note Created")
          onSuccess?.()
        },
        onError: (err: Error) => {
          handleError.call(showErrorToast, err as ApiError)
        },
      })
    }
  }

  if (isLoadingPolicy || (riskNoteId && isLoadingRiskNote)) {
    return <div className="p-8 text-center">Loading form details...</div>
  }

  const productAny = policy?.product as any
  const productDetails = (productAny?.product_details as any[]) || []

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit as any)} className="space-y-6">
        <div className="space-y-4 bg-muted/30 p-4 rounded-lg">
          <FormField
            control={form.control as any}
            name="transaction_type"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Transaction Type</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="New Business">New Business</SelectItem>
                    <SelectItem value="Renewal">Renewal</SelectItem>
                    <SelectItem value="Cancellation">Cancellation</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control as any}
            name="status"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Status</FormLabel>
                <Select
                  onValueChange={field.onChange}
                  defaultValue={field.value}
                >
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select status" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="Draft">Draft (Preliminary)</SelectItem>
                    <SelectItem value="Renewal Invited">Renewal Invited</SelectItem>
                    <SelectItem value="Renewal Confirmed">
                      Renewal Confirmed
                    </SelectItem>
                    <SelectItem value="Active">Active (Finalized)</SelectItem>
                    <SelectItem value="Cancelled">Cancelled</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <FormField
            control={form.control as any}
            name="coverage_start"
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
            control={form.control as any}
            name="coverage_end"
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

        <div className="space-y-4">
          <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground border-b pb-1">
            Risk Details ({policy?.product?.class_of_insurance})
          </h3>
          <div className="grid grid-cols-1 gap-4">
            {productDetails
              .filter(
                (f: any) =>
                  f.field_type === "input" || f.field_type === "optional",
              )
              .map((field: any) => (
                <FormField
                  key={field.key}
                  control={form.control as any}
                  name={`details.${field.key}`}
                  render={({ field: inputField }) => (
                    <FormItem>
                      <FormLabel>{field.label}</FormLabel>
                      <FormControl>
                        <Input
                          type={field.type === "number" ? "number" : "text"}
                          {...inputField}
                          value={inputField.value || ""}
                          onChange={(e) =>
                            inputField.onChange(
                              field.type === "number"
                                ? e.target.valueAsNumber
                                : e.target.value,
                            )
                          }
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              ))}
          </div>
        </div>

        <div className="space-y-4 pt-4 border-t">
          <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground border-b pb-1">
            Financials
          </h3>
          <div className="space-y-4">
            <FormField
              control={form.control as any}
              name="net_premium"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Net Premium (KSH)</FormLabel>
                  <FormControl>
                    <Input type="number" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control as any}
              name="commission_amount"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Commission (KSH)</FormLabel>
                  <FormControl>
                    <Input type="number" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>
        </div>

        <div className="flex justify-end gap-4 pt-4">
          <Button type="button" variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <LoadingButton
            type="submit"
            loading={updateRiskNote.isPending || createRiskNote.isPending}
            className="font-bold"
          >
            {form.watch("status") === "Active"
              ? "Issue Risk Note"
              : "Save Draft Changes"}
          </LoadingButton>
        </div>
      </form>
    </Form>
  )
}
