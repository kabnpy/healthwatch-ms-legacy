# Strategy: Semantic Risk Note Rendering

## Goal
Refactor the Risk Note document rendering to use semantic HTML tables, ensuring all cover details are visible, professionally formatted, and maintainable.

## 1. Architectural Approach
- **Semantic Tables**: Use `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th>`, and `<td>` for all data sections.
- **Data-Driven Sections**: Automatically generate sections based on the `policy_snapshot.risk_details` structure.
- **Hierarchical Layout**: Distinguish between "Section Headers" (full-width) and "Key-Value Pairs" (2-column).
- **Graceful Fallbacks**: Handle missing or empty data without breaking the document flow.

## 2. Measurable Steps

### Phase 1: Semantic Foundation
- [x] **Step 1.1**: Create `frontend/src/components/Documents/templates/RiskNote/RiskNoteTable.tsx` as a replacement for the recursive renderer.
- [x] **Step 1.2**: Implement a `TableSection` component that renders a section header and a `<tbody>` of rows. (Implemented within RiskNoteTable)
- [x] **Step 1.3**: Implement a `TableRow` component for consistent key-value alignment. (Implemented within RiskNoteTable)

### Phase 2: Data Mapping & Visibility
- [x] **Step 2.1**: Update `RiskNoteTemplate.tsx` to pass the raw `policy_snapshot.risk_details` to the new table component.
- [x] **Step 2.2**: Implement logic to handle nested objects (e.g., "VEHICLE DETAILS" as a sub-table).
- [x] **Step 2.3**: Verify that all fields from the `Product` form schema appear correctly in the output.

### Phase 3: Professional Formatting
- [x] **Step 3.1**: Standardize typography (uppercase keys, bold values, monospace for reference numbers).
- [x] **Step 3.2**: Add print-specific CSS to ensure tables don't break awkwardly across pages. (Handled via table-collapse and BaseDocument structure)
- [x] **Step 3.3**: Ensure the financial summary table matches the aesthetic of the cover details.

### Phase 4: Verification
- [x] **Step 4.1**: Compare Motor, PA, and Domestic Risk Notes against legacy manual templates.
- [x] **Step 4.2**: Verify "Edit Draft" functionality with the new table structure.
- [x] **Step 4.3**: Achieve a clean build and no console errors during rendering.

---

## 3. Implementation Details

### Semantic Structure Example:
```html
<table class="w-full border-t border-black">
  <thead>
    <tr class="bg-gray-100">
      <th colspan="2" class="text-left py-1 px-4 text-[10px] uppercase tracking-widest">Section Name</th>
    </tr>
  </thead>
  <tbody>
    <tr class="border-b border-gray-200">
      <td class="py-2 px-4 font-bold text-[11px] w-1/3">LABEL</td>
      <td class="py-2 px-4 text-[11px]">VALUE</td>
    </tr>
  </tbody>
</table>
```
