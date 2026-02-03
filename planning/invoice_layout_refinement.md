# Strategy: Invoice Layout Refinement

## Objective
Refine the `InvoiceTemplate` to achieve visual consistency with the `RiskNoteTemplate` by utilizing existing design patterns and components (`RiskNoteRow`, `RiskNoteSection`, etc.).

## Visual Direction
1. **Consistency**: Use the same grid-based key-value rows (`RiskNoteRow`) for header details.
2. **Tabular Data**: Replace the current simple grid with a more structured table that matches the "Risk Note" border style.
3. **Typography & Spacing**: Standardize font sizes (e.g., `text-[10px]` for labels, `text-[11px]` for values) and border weights.

## Proposed Layout Structure

### 1. Document Header
- **Title**: "DEBIT NOTE" (Standard for Insurance Invoices) or "TAX INVOICE".
- **Reference**: `invoiceref` (Invoice Number) styled exactly like the Risk Note's Ref.

### 2. Core Information Section (Using `RiskNoteRow`)
- **Client**: Name, Postal Address, City, and PIN.
- **Invoice Date**: Formatted as a year range (e.g., `2025/2026`).
- **Insurer**: The carrier associated with the policies.

### 3. The Insurance Table
A 4-column grid matching the Risk Note's internal borders:
- **Col 1 (1/12)**: Item Number (#).
- **Col 2 (4/12)**: Class of Insurance.
- **Col 3 (5/12)**: Policy Number & Period (combined in one cell for density).
- **Col 4 (2/12)**: Annual Premium (Right-aligned).

### 4. Financial Summary
- **Total Premium**: Large, bold total at the bottom right.
- **Balance Due**: Highlighted if different from Total.

---

## Measurable Goals

- [x] **Goal 1: Header & Meta Data Alignment**
  - Update `InvoiceTemplate` to use `RiskNoteRow` for Client, Insurer, and Date info.
  - Implement the `YYYY/YYYY+1` date formatting logic.
- [x] **Goal 2: Specialized Invoice Table Row**
  - Create `InvoiceTableRow.tsx` or adapt `RiskNoteGridRow` to support the 4-column structure.
  - Ensure borders and padding match exactly.
- [x] **Goal 3: Data Plumbing**
  - Ensure `lineItems` passed to `InvoiceTemplate` include necessary `RiskNote` and `Policy` details (Class, Policy No, Period).
- [x] **Goal 4: Final Polish**
  - Apply the "Minimal Invoice" styling to the footer (Payment Instructions).
  - Run linting and formatting.

## Git & Branching Strategy
- **Branch**: `feature/refine-invoice-layout`
- **Commits**:
  - `docs: add invoice refinement strategy`
  - `feat(frontend): update invoice header to match risk note style`
  - `feat(frontend): implement 4-column invoice table layout`
  - `fix(frontend): refine invoice date formatting and data mapping`
