import { getSectionLayout } from "@/utils/layoutRegistry"
import { BaseDocument } from "../BaseDocument"
import { RiskNoteGridRow } from "./RiskNote/RiskNoteGridRow"
import { RiskNoteListItem } from "./RiskNote/RiskNoteListItem"
import { RiskNoteRow } from "./RiskNote/RiskNoteRow"
import { RiskNoteSection } from "./RiskNote/RiskNoteSection"

interface RiskNoteTemplateProps {
  riskNote: any
  client: any
  policy: any
}

export const RiskNoteTemplate = ({
  riskNote,
  client,
  policy,
}: RiskNoteTemplateProps) => {
  // Extract snapshot data
  const items = (riskNote.items_snapshot?.items as any[]) || []
  const riskItem = items[0] || {}
  const productDetails = (policy.product?.product_details as any[]) || []
  const details = riskItem.details || {}

  // Aggregate fields by "section" metadata in productDetails
  const dynamicSections = productDetails.reduce(
    (acc: Record<string, any[]>, field: any) => {
      let displayValue = null

      if (field.field_type === "static") {
        displayValue = field.value
      } else if (field.field_type === "input") {
        const val = details[field.key]
        if (val !== undefined && val !== null && val !== "") {
          displayValue = val
        }
      } else if (field.field_type === "optional") {
        displayValue = details[field.key] || field.value
      }

      if (displayValue !== null && field.show_in_risknote !== false) {
        const sectionName = field.section || "Additional Details"
        if (!acc[sectionName]) acc[sectionName] = []
        acc[sectionName].push({
          label: field.label,
          value: displayValue,
        })
      }
      return acc
    },
    {},
  )

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat("en-KE", {
      style: "currency",
      currency: "KSH",
    }).format(amount)
  }

  return (
    <BaseDocument>
      <div className="space-y-4">
        {/* Document Header Info */}
        <div className="flex justify-between items-start border-b-2 border-black pb-4">
          <div>
            <h1 className="text-2xl font-black uppercase tracking-tighter">
              Risk Note
            </h1>
            <p className="text-[10px] text-gray-500 font-mono uppercase">
              Ref: {riskNote.invoice_number || "DRAFT"}
            </p>
          </div>
          <div className="text-right">
            <div
              className={`px-2 py-0.5 text-[10px] font-bold uppercase rounded ${
                riskNote.status === "Draft"
                  ? "bg-yellow-100 text-yellow-800"
                  : "bg-green-100 text-green-800"
              }`}
            >
              {riskNote.status}
            </div>
          </div>
        </div>

        {/* CORE DETAILS SECTION */}
        <div className="mt-6 border-t border-black">
          <RiskNoteRow
            label="Insured"
            value={
              <div className="font-bold">
                <p>{client.name}</p>
                <p className="text-[10px] text-gray-500 font-normal">
                  PIN: {client.kra_pin || "N/A"}
                </p>
                <p className="text-[10px] text-gray-500 font-normal">
                  {client.postal_address} {client.city}
                </p>
              </div>
            }
          />
          <RiskNoteRow
            label="Class"
            value={
              <div className="flex justify-between items-center w-full">
                <span className="font-bold">
                  {policy.product?.class_of_insurance || "N/A"}
                </span>
                <span className="text-[10px] bg-gray-100 px-2 py-0.5 rounded">
                  Policy No: {policy.policy_number}
                </span>
              </div>
            }
          />
          <RiskNoteRow
            label="Period"
            value={
              <div className="font-bold">
                {new Date(riskNote.start_date).toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "long",
                  year: "numeric",
                })}{" "}
                To{" "}
                {new Date(riskNote.end_date).toLocaleDateString("en-GB", {
                  day: "numeric",
                  month: "long",
                  year: "numeric",
                })}
              </div>
            }
          />
          <RiskNoteRow
            label="Cover"
            value={
              <div className="text-[11px] leading-relaxed italic text-gray-700">
                {riskItem.cover || "As per policy terms and conditions."}
              </div>
            }
          />
        </div>

        {/* DYNAMIC SECTIONS FROM FORM_SCHEMA */}
        {Object.entries(dynamicSections).map(([sectionName, fields]) => {
          const config = getSectionLayout(sectionName, fields.length)

          if (config.layout === "grid-row") {
            return (
              <RiskNoteGridRow
                key={sectionName}
                label={sectionName}
                fields={fields.map((f) => ({
                  label: f.label,
                  value:
                    typeof f.value === "number" &&
                    f.label.toLowerCase().includes("value")
                      ? formatCurrency(f.value)
                      : f.value,
                }))}
              />
            )
          }

          const isGridSection = config.layout === "list-item" && fields.length > 4

          return (
            <RiskNoteSection key={sectionName} title={sectionName}>
              <div className={isGridSection ? "grid grid-cols-2" : ""}>
                {fields.map((field, idx) =>
                  config.layout === "list-item" ? (
                    <RiskNoteListItem
                      key={idx}
                      label={field.label}
                      value={field.value}
                      noBorderRight={isGridSection && idx % 2 === 0}
                      showLabel={
                        config.showLabelInList &&
                        field.value !== "Included" &&
                        field.value !== "Yes"
                      }
                    />
                  ) : (
                    <RiskNoteRow
                      key={idx}
                      label={field.label}
                      value={
                        typeof field.value === "number" &&
                        field.label.toLowerCase().includes("value")
                          ? formatCurrency(field.value)
                          : field.value
                      }
                    />
                  ),
                )}
              </div>
            </RiskNoteSection>
          )
        })}

        {/* FINANCIAL SUMMARY */}
        <div className="mt-8 border-t-2 border-black pt-4">
          <div className="ml-auto w-1/2">
            <RiskNoteRow
              label="Premium"
              value={formatCurrency(riskNote.net_premium)}
              className="border-t border-black"
              labelClassName="bg-transparent"
            />
            {Object.entries(riskNote.taxes || {}).map(
              ([taxName, amount]: [string, any]) => (
                <RiskNoteRow
                  key={taxName}
                  label={taxName.replace(/([A-Z])/g, " $1")}
                  value={formatCurrency(amount)}
                  labelClassName="bg-transparent"
                />
              ),
            )}
            <RiskNoteRow
              label="Annual Premium"
              value={
                <span className="text-sm font-black">
                  {formatCurrency(riskNote.total_amount)}
                </span>
              }
              labelClassName="bg-gray-100"
              valueClassName="bg-gray-100"
            />
          </div>
        </div>

        {/* INSURER FOOTER */}
        <div className="mt-12 text-[11px]">
          <RiskNoteRow
            label="Insurer"
            value={
              <span className="font-bold">
                {policy.product?.insurer?.name || "N/A"}
              </span>
            }
            className="border-t border-b-0"
          />
        </div>
      </div>
    </BaseDocument>
  )
}
