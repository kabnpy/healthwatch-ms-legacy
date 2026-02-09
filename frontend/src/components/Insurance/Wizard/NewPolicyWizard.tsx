import { useMemo, useState } from "react"
import { RiskNotesService } from "@/client"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import useCustomToast from "@/hooks/useCustomToast"
import {
  useCreatePolicy,
  useCreateRiskNote,
  useUpdateRiskNote,
  useProducts,
} from "@/hooks/useInsurance"
import { StepAsset } from "./StepAsset"
import { StepBlueprint } from "./StepBlueprint"
import { StepFinancials } from "./StepFinancials"
import { StepReview } from "./StepReview"
import { cn } from "@/lib/utils"

const steps = ["Product", "Details", "Financials", "Review"]

interface NewPolicyWizardProps {
  clientId: string
  isOpen: boolean
  onClose: () => void
  onSuccess?: () => void
}

export function NewPolicyWizard({
  clientId,
  isOpen,
  onClose,
  onSuccess,
}: NewPolicyWizardProps) {
  const [step, setStep] = useState(0)
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const { data: productsData } = useProducts()

  const createPolicy = useCreatePolicy()
  const createRiskNote = useCreateRiskNote()
  const updateRiskNote = useUpdateRiskNote()

  const [state, setState] = useState<any>({
    product_id: "",
    details: {},
    financials: {
      sumInsured: 0,
      rate: 4.5,
      startDate: new Date().toISOString().split("T")[0],
      duration: 12,
    },
    extensions: {
      pvt: false,
      excessProtector: false,
      passengerLiability: false,
    },
  })

  const selectedProduct = useMemo(() => {
    return productsData?.data.find((p) => p.id === state.product_id)
  }, [state.product_id, productsData])

  const handleNext = (data: any) => {
    if (step === 0) {
      setState((prev: any) => ({ ...prev, product_id: data.product_id }))
    } else if (step === 1) {
      // Sync logic: Extract "Value" or "Sum Insured" from details
      let extractedValue = 0
      const detailKeys = Object.keys(data)
      const valueKey = detailKeys.find((k) => /value|sum insured/i.test(k))

      if (valueKey) {
        const val = data[valueKey]
        // Remove currency symbols/commas if string, then parse
        const cleanVal =
          typeof val === "string" ? val.toString().replace(/[^0-9.]/g, "") : val
        extractedValue = Number(cleanVal) || 0
      }

      setState((prev: any) => ({
        ...prev,
        details: data,
        financials: {
          ...prev.financials,
          sumInsured:
            extractedValue > 0 ? extractedValue : prev.financials.sumInsured,
        },
      }))
    } else {
      setState((prev: any) => ({ ...prev, ...data }))
    }
    setStep((s) => s + 1)
  }

  const handleBack = () => {
    setStep((s) => s - 1)
  }

  const handleIssuePolicy = async () => {
    try {
      if (!selectedProduct) throw new Error("No product selected")

      // 1. Calculate Financials
      const { calculatePremium } = await import("@/lib/calculator")
      const calc = calculatePremium({
        sumInsured: state.financials?.sumInsured || 0,
        rate: state.financials?.rate || 0,
        hasPVT: state.extensions?.pvt || false,
        hasExcessProtector: state.extensions?.excessProtector || false,
      })

      const startDate = state.financials?.startDate || new Date().toISOString().split("T")[0]
      const endDate = new Date(
        new Date(startDate).setFullYear(
          new Date(startDate).getFullYear() + 1,
        ),
      ).toISOString().split("T")[0]

      // 2. Create Policy with all details (This auto-creates a Draft Risk Note in backend)
      console.log("Creating policy with data:", {
        policy_number: `P/${Math.floor(Math.random() * 1000000)}`,
        client_id: clientId,
        product_id: state.product_id,
        status: "Active",
        start_date: startDate,
        end_date: endDate,
        description: state.details?.description || selectedProduct.name,
        total_premium: calc.breakdown.total,
        premium_breakdown: calc.breakdown as any,
        risk_details: state.details,
      })
      const policy = await createPolicy.mutateAsync({
        policy_number: `P/${Math.floor(Math.random() * 1000000)}`,
        client_id: clientId,
        product_id: state.product_id,
        status: "Active",
        start_date: startDate,
        end_date: endDate,
        description: state.details?.description || selectedProduct.name,
        total_premium: calc.breakdown.total,
        premium_breakdown: calc.breakdown as any,
        risk_details: state.details,
      })
      console.log("Policy created successfully:", policy)

      // 3. Finalize Risk Note
      // FIND THE AUTO-CREATED DRAFT RISK NOTE
      console.log("Fetching draft risk note for policy:", policy.id)
      const riskNotesResponse = await RiskNotesService.readRiskNotes({ policyId: policy.id })
      console.log("Risk notes found:", riskNotesResponse.data)
      const draftRiskNote = riskNotesResponse.data.find(rn => rn.status === "Draft")

      if (draftRiskNote) {
        console.log("Updating draft risk note:", draftRiskNote.id)
        await updateRiskNote.mutateAsync({
          id: draftRiskNote.id,
          data: {
            transaction_type: "New Business",
            start_date: startDate,
            end_date: endDate,
            net_premium: calc.breakdown.basic + (calc.breakdown.extensions?.reduce((acc: number, curr: any) => acc + curr.amount, 0) || 0),
            taxes: calc.breakdown.levies as any,
            commission_amount: calc.breakdown.basic * ((selectedProduct.default_commission_rate || 10.0) / 100),
            total_amount: calc.breakdown.total,
            status: "Active",
            policy_snapshot: {
                id: policy.id,
                policy_number: policy.policy_number,
                client_id: policy.client_id,
                product_id: policy.product_id,
                status: policy.status,
                start_date: policy.start_date,
                end_date: policy.end_date,
                description: policy.description,
                total_premium: policy.total_premium,
                risk_details: policy.risk_details,
                premium_breakdown: policy.premium_breakdown,
            },
            special_clauses: [],
          }
        })
        console.log("Risk note updated successfully")
      } else {
        console.warn("No draft risk note found to update")
      }

      showSuccessToast("Policy Issued Successfully!")
      onSuccess?.()
      onClose()
    } catch (err: any) {
      console.error("Policy Issuance Error:", err)
      let message = "Failed to issue policy"
      if (err.body?.detail) {
        message = typeof err.body.detail === 'string' ? err.body.detail : JSON.stringify(err.body.detail)
      }
      showErrorToast(message)
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>Issue New Policy - {steps[step]}</DialogTitle>
        </DialogHeader>

        <div className="py-4">
          {/* Progress Bar */}
          <div className="flex justify-between mb-8">
            {steps.map((s, i) => (
              <div key={i} className="flex flex-col items-center flex-1">
                <div
                  className={`size-8 rounded-full flex items-center justify-center text-sm font-bold transition-colors ${i <= step ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"}`}
                >
                  {i + 1}
                </div>
                <span className={cn("text-[10px] mt-1 font-bold uppercase tracking-wider", i <= step ? "text-primary" : "text-muted-foreground")}>{s}</span>
              </div>
            ))}
          </div>

          {step === 0 && (
            <StepAsset
              defaultValues={{ product_id: state.product_id }}
              onNext={handleNext}
            />
          )}
          {step === 1 && (
            <StepBlueprint
              productId={state.product_id}
              defaultValues={state.details}
              onNext={handleNext}
              onBack={handleBack}
            />
          )}
          {step === 2 && (
            <StepFinancials
              productId={state.product_id || ""}
              defaultValues={{
                financials: state.financials,
                extensions: state.extensions,
              }}
              onNext={handleNext}
              onBack={handleBack}
            />
          )}
          {step === 3 && (
            <StepReview
              state={state}
              onIssue={handleIssuePolicy}
              onBack={handleBack}
              isSubmitting={
                createPolicy.isPending ||
                createRiskNote.isPending
              }
            />
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}