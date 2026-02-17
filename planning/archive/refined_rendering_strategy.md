# Strategy: Refined Semantic Document Rendering

## Goal
Improve the visual consistency and semantic structure of all document tables. Ensure that static product information (benefits, clauses) from `product_details` is rendered alongside captured `risk_details`.

## 1. Architectural Refinements
- **Semantic Headers**: Convert label columns from `<td>` to `<th scope="row">`.
- **Data Aggregation**: The Risk Note should render a union of:
    1.  **Template Data**: Static content from `policy.product.product_details` (e.g., Benefits, Exclusions).
    2.  **Instance Data**: Captured fields in `policy_snapshot.risk_details` (e.g., Reg No, Sum Insured).
- **Uniform Styling**: Apply the "Clean Bordered" look consistently across all tables (Header, Risk, Financials, Insurer).

## 2. Measurable Steps

### Phase 1: Semantic Table Component
- [x] **Step 1.1**: Update `RiskNoteTable.tsx` to use `<th scope="row">` for labels.
- [x] **Step 1.2**: Apply consistent styling: `border border-black`, `bg-slate-50` for headers, `p-2` padding.
- [x] **Step 1.3**: Add logic to handle "List" values (arrays) in `product_details`.

### Phase 2: Template Data Integration
- [x] **Step 2.1**: Update `RiskNoteTemplate.tsx` to merge `product_details` and `risk_details` before passing them to the renderer.
- [x] **Step 2.2**: Ensure that `product_details` (template) fields are correctly populated with values from `risk_details` (instance) where applicable.
- [x] **Step 2.3**: Fix visibility issue: Ensure sections like "BENEFITS" and "EXCESS" appear in the output.

### Phase 3: Global Template Refactor
- [x] **Step 3.1**: Refactor the "Header Table" in `RiskNoteTemplate` and `InvoiceTemplate` to use the new semantic structure.
- [x] **Step 3.2**: Refactor the "Financial Summary Table" to match.
- [x] **Step 3.3**: Refactor the "Insurer/Footer Table" to match.

### Phase 4: Verification
- [ ] **Step 4.1**: Verify that "VEHICLE DETAILS" shows captured data.
- [ ] **Step 4.2**: Verify that "BENEFITS" shows the fixed text from the catalog.
- [ ] **Step 4.3**: Clean build and print test.

---

## 3. Data Merging Logic
We will use a helper to merge the template structure with instance data:
```typescript
const mergedData = {
  ...product_details, // e.g. { "BENEFITS": { "Accidental Death": "500k" } }
  ...risk_details     // e.g. { "VEHICLE DETAILS": { "Reg No": "KCA 123" } }
}
```
If sections overlap, we will intelligently merge their inner key-value pairs.
