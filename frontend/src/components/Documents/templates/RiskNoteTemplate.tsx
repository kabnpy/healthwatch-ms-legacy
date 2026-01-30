import { BaseDocument } from "../BaseDocument";

interface RiskNoteTemplateProps {
  riskNote: any;
  client: any;
  policy: any;
}

export const RiskNoteTemplate = ({
  riskNote,
  client,
  policy,
}: RiskNoteTemplateProps) => {
  // Extract snapshot data
  const items = (riskNote.items_snapshot?.items as any[]) || [];
  const riskItem = items[0] || {};
  const formSchema = (policy.product?.form_schema as any[]) || [];
  const details = riskItem.details || {};

  // Aggregate fields by category
  const aggregatedGroups = formSchema.reduce(
    (acc: Record<string, any[]>, field: any) => {
      const value = details[field.key];
      if (value !== undefined && value !== null && value !== "") {
        const category = field.category || "General";
        if (!acc[category]) acc[category] = [];
        acc[category].push({ label: field.label, value });
      }
      return acc;
    },
    {},
  );

  const taxes = riskNote.taxes || {};

  return (
    <BaseDocument>
      <div>
        <h2>Risk Note</h2>
        <p>Client: {client.name}</p>
        <p>Policy: {policy.name}</p>
        <p>Risk Item: {riskItem.name}</p>
        <p>Taxes: {taxes.amount}</p>
      </div>
    </BaseDocument>
  );
};
