import { useState } from "react"
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import useCustomToast from "@/hooks/useCustomToast"
import {
  useCreatePolicy,
  useCreateRiskItem,
  useCreateRiskNote,
} from "@/hooks/useInsurance"
import type { WizardState } from "@/types/wizard"
import { StepAsset } from "./StepAsset"
import { StepFinancials } from "./StepFinancials"
import { StepReview } from "./StepReview"

const steps = ["Asset Details", "Coverage & Financials", "Review"]

interface NewBusinessWizardProps {
  clientId: string
  isOpen: boolean
  onClose: () => void
  onSuccess?: () => void
}

export function NewBusinessWizard({
  clientId,
  isOpen,
  onClose,
  onSuccess,
}: NewBusinessWizardProps) {
  const [step, setStep] = useState(0)
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const createPolicy = useCreatePolicy()
  const createRiskItem = useCreateRiskItem()
  const createRiskNote = useCreateRiskNote()

  const [state, setState] = useState<Partial<WizardState>>({
    product_id: "",
    asset: {
      identifier: "",
      description: "",
      details: {},
    },
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
    benefitOverrides: {},
  })

  const handleNext = (data: any) => {
    setState((prev) => ({ ...prev, ...data }))
    setStep((s) => s + 1)
  }

  const handleBack = () => {
    setStep((s) => s - 1)
  }

  const handleIssuePolicy = async () => {
    try {
      // 1. Create Policy
      const policy = await createPolicy.mutateAsync({
        policy_number: `P/${Math.floor(Math.random() * 1000000)}`,
        client_id: clientId,
        product_id: state.product_id,
        status: "Active",
      })

      // 2. Create Risk Item
      await createRiskItem.mutateAsync({
        policyId: policy.id,
        data: {
          policy_id: policy.id,
          description: state.asset?.description || "",
          cover_description: "Comprehensive", // Default
          total_premium: 0, // Calculated later
          premium_breakdown: {},
          risk_details: {
            ...state.asset?.details,
            identifier: state.asset?.identifier,
            sum_insured: state.financials?.sumInsured || 0,
          },
          version_number: 1,
          is_active: true,
        },
      })

      // 3. Create Risk Note
      const { calculatePremium } = await import("@/lib/calculator")
      const calc = calculatePremium({
        sumInsured: state.financials?.sumInsured || 0,
        rate: state.financials?.rate || 4.5,
        hasPVT: state.extensions?.pvt || false,
        hasExcessProtector: state.extensions?.excessProtector || false,
        hasPassengerLiability: state.extensions?.passengerLiability || false,
      })

      await createRiskNote.mutateAsync({
        policy_id: policy.id,
        transaction_type: "New Business",
        start_date: state.financials?.startDate || "",
        end_date: new Date(
          new Date(state.financials?.startDate || "").setFullYear(
            new Date(state.financials?.startDate || "").getFullYear() + 1,
          ),
        )
          .toISOString()
          .split("T")[0],
        net_premium:
          calc.breakdown.basic +
          calc.breakdown.extensions.reduce((acc, curr) => acc + curr.amount, 0),
        taxes: calc.breakdown.levies as any,
        commission_amount: calc.breakdown.basic * 0.125,
        total_amount: calc.breakdown.total,
        items_snapshot: {
          items: [state.asset],
        },
        special_clauses: [],
      })

      showSuccessToast("Policy Issued Successfully!")
      onSuccess?.()
      onClose()
    } catch (_error) {
      showErrorToast("Failed to issue policy")
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            New Business Wizard - Step {step + 1}: {steps[step]}
          </DialogTitle>
        </DialogHeader>

        <div className="py-4">
          {/* Progress Bar */}
          <div className="flex justify-between mb-8">
            {steps.map((s, i) => (
              <div key={i} className="flex flex-col items-center flex-1">
                <div
                  className={`size-8 rounded-full flex items-center justify-center text-sm font-bold ${i <= step ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground"}`}
                >
                  {i + 1}
                </div>
                <span className="text-xs mt-1">{s}</span>
              </div>
            ))}
          </div>

          {step === 0 && (
            <StepAsset
              defaultValues={{
                product_id: state.product_id,
                asset: state.asset,
              }}
              onNext={(data) => handleNext(data)}
            />
          )}
          {step === 1 && (
            <StepFinancials
              defaultValues={{
                financials: state.financials,
                extensions: state.extensions,
              }}
              onNext={(data) => handleNext(data)}
              onBack={handleBack}
            />
          )}
          {step === 2 && (
            <StepReview
              state={state as WizardState}
              onIssue={handleIssuePolicy}
              onBack={handleBack}
              isSubmitting={
                createPolicy.isPending ||
                createRiskItem.isPending ||
                createRiskNote.isPending
              }
            />
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
