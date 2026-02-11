import { RefreshCcw, Save } from "lucide-react"
import { useCallback, useEffect, useMemo, useState } from "react"
import type { ClientPublic } from "@/client"
import { Button } from "@/components/ui/button"
import type {
  EnhancedPolicy,
  EnhancedRiskNote,
  RiskNoteContentValue,
  RiskNoteSection,
} from "@/types/insurance"
import { BaseDocument } from "../BaseDocument"
import { RiskNoteTable } from "./RiskNote/RiskNoteTable"

interface RiskNoteTemplateProps {
  riskNote: EnhancedRiskNote
  client: ClientPublic
  policy: EnhancedPolicy
  isEditable?: boolean
  onSave?: (updatedSnapshot: any) => void
}

export const RiskNoteTemplate = ({
  riskNote,
  client,
  policy,
  isEditable = false,
  onSave,
}: RiskNoteTemplateProps) => {
  const [localSnapshot, setLocalSnapshot] = useState<Record<string, any>>(
    riskNote.policy_snapshot || {},
  )

  // Keep local state in sync with external changes if not editing
  useEffect(() => {
    if (!isEditable) {
      setLocalSnapshot(riskNote.policy_snapshot || {})
    }
  }, [riskNote.policy_snapshot, isEditable])

  const formatCurrency = useCallback((amount: number) => {
    return new Intl.NumberFormat("en-KE", {
      style: "currency",
      currency: "KSH",
    }).format(amount)
  }, [])

  const handleSave = () => {
    onSave?.(localSnapshot)
  }

  const handleReset = () => {
    setLocalSnapshot(riskNote.policy_snapshot || {})
  }

  // --- DATA CONSOLIDATION LOGIC ---
  const tableSections = useMemo(() => {
    const sections: RiskNoteSection[] = []

    // 1. INSURED
    sections.push({
      name: "INSURED",
      content: (
        <div className="text-black">
          <p className="font-bold text-base leading-tight mb-1">
            {client.name}
          </p>
          <div className="flex justify-between items-start gap-8">
            <p className="text-[11px] leading-relaxed">
              {client.postal_number
                ? `P.O. Box ${client.postal_number}`
                : "No Address Provided"}
              {client.postal_code && ` - ${client.postal_code}`}
              <br />
              {client.town || "Nairobi"}
            </p>
            <p className="font-mono text-[11px] font-bold shrink-0">
              P.I.N No. {client.kra_pin || "N/A"}
            </p>
          </div>
        </div>
      ),
    })

    // 2. CLASS
    sections.push({
      name: "CLASS",
      content: (
        <div className="flex justify-between items-center w-full text-black">
          <span className="font-bold uppercase tracking-tight">
            {policy.product?.name || "N/A"}
          </span>
          <span className="font-mono text-[11px] font-bold">
            [Policy No. {policy.policy_number}]
          </span>
        </div>
      ),
    })

    // 3. PERIOD
    sections.push({
      name: "PERIOD",
      content: (
        <div className="flex items-center gap-12 text-black font-bold uppercase tracking-tight">
          <span>
            {new Date(riskNote.start_date).toLocaleDateString("en-GB", {
              day: "numeric",
              month: "long",
              year: "numeric",
            })}
          </span>
          <span className="text-slate-400 normal-case font-normal italic">
            To
          </span>
          <span>
            {new Date(riskNote.end_date).toLocaleDateString("en-GB", {
              day: "numeric",
              month: "long",
              year: "numeric",
            })}
          </span>
        </div>
      ),
    })

    // 4. COVER
    sections.push({
      name: "COVER",
      content: (
        <div className="text-black text-[11px] leading-relaxed italic">
          {policy.product?.class_of_insurance}: Accidental loss or damage to
          insured property and / or death, bodily injury or loss or damage to
          property of third parties.
        </div>
      ),
    })

    // 5. DYNAMIC RISK SECTIONS (Template + Instance)
    const template: Record<string, any> = policy.product?.product_details || {}
    const instance: Record<string, any> = localSnapshot.risk_details || {}

    // Merge logic: template provides structure, instance provides values
    // We iterate over the template sections to ensure order and grouping
    const manualSections = [
      "INSURED",
      "CLASS",
      "PERIOD",
      "COVER",
      "ANNUAL PREMIUM",
      "FINANCIAL SUMMARY",
      "INSURER",
      "AUTHENTICATION",
    ]

    // First, handle sections defined in the template
    Object.entries(template).forEach(([name, templateContent]) => {
      const upperName = name.toUpperCase()
      if (!manualSections.includes(upperName)) {
        const instanceContent = instance[name] || instance[upperName] || {}

        let mergedContent = templateContent
        if (typeof templateContent === "object" && templateContent !== null) {
          // If it's a structured section (like VEHICLE DETAILS)
          mergedContent = { ...templateContent }
          if (typeof instanceContent === "object" && instanceContent !== null) {
            Object.entries(instanceContent).forEach(([k, v]) => {
              // Only override if the value is not a placeholder or if it has actual data
              if (
                v !== undefined &&
                v !== null &&
                v !== "" &&
                v !== "[ EMPTY ]"
              ) {
                mergedContent[k] = v
              }
            })
          }
        } else if (instanceContent && instanceContent !== "[ EMPTY ]") {
          mergedContent = instanceContent
        }

        sections.push({
          name: upperName,
          content: mergedContent as RiskNoteContentValue,
        })
      }
    })

    // Then, add any sections from instance that weren't in template (fallback for legacy/custom)
    Object.entries(instance).forEach(([name, content]) => {
      const upperName = name.toUpperCase()
      if (
        !manualSections.includes(upperName) &&
        !sections.find((s) => s.name === upperName)
      ) {
        sections.push({
          name: upperName,
          content: content as RiskNoteContentValue,
        })
      }
    })

    // 6. ANNUAL PREMIUM
    const taxRows: Record<string, RiskNoteContentValue> = {}
    Object.entries(riskNote.taxes || {}).forEach(([name, amt]) => {
      taxRows[name.replace(/([A-Z])/g, " $1")] = formatCurrency(amt as number)
    })

    sections.push({
      name: "ANNUAL PREMIUM",
      content: {
        Premium: formatCurrency(riskNote.net_premium),
        ...taxRows,
        "Total Amount Payable": (
          <span className="text-[13px] font-black text-black">
            {formatCurrency(riskNote.total_amount)}
          </span>
        ),
      },
    })

    // 7. INSURER
    sections.push({
      name: "INSURER",
      content: (
        <div className="flex justify-between items-center text-black">
          <span className="font-bold uppercase text-[11px]">
            {policy.product?.insurer?.name || "N/A"}
          </span>
        </div>
      ),
    })

    return sections
  }, [client, policy, riskNote, localSnapshot.risk_details, formatCurrency])

  const handleUpdateSection = (sectionName: string, updatedContent: any) => {
    setLocalSnapshot({
      ...localSnapshot,
      risk_details: {
        ...localSnapshot.risk_details,
        [sectionName]: updatedContent,
      },
    })
  }

  return (
    <div className="relative group">
      {/* EDITING TOOLBAR */}
      {isEditable && (
        <div className="absolute -top-12 left-0 right-0 flex justify-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity z-30">
          <Button
            size="sm"
            variant="outline"
            className="bg-white shadow-sm"
            onClick={handleReset}
          >
            <RefreshCcw className="h-3 w-3 mr-2" /> Reset
          </Button>
          <Button size="sm" className="shadow-sm" onClick={handleSave}>
            <Save className="h-3 w-3 mr-2" /> Save Draft Changes
          </Button>
        </div>
      )}

      <BaseDocument>
        <div className="space-y-4">
          {/* Document Header Info */}
          <div className="flex justify-between items-start border-b-2 border-black pb-4">
            <div>
              <h1 className="text-2xl font-black uppercase tracking-tighter text-black">
                Risk Note
              </h1>
              <p className="text-[10px] text-slate-500 font-mono uppercase">
                Ref: {riskNote.risk_note_number || "DRAFT"}
              </p>
            </div>
            <div className="text-right">
              <div
                className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded border ${
                  riskNote.status === "Draft"
                    ? "bg-amber-100 text-amber-800 border-amber-200"
                    : "bg-emerald-100 text-emerald-800 border-emerald-200"
                }`}
              >
                {riskNote.status}
              </div>
            </div>
          </div>

          {/* UNIFIED TABLE BODY */}
          <div className="mt-2">
            <RiskNoteTable
              sections={tableSections}
              isEditable={isEditable}
              onChange={handleUpdateSection}
            />
          </div>
        </div>
      </BaseDocument>
    </div>
  )
}
