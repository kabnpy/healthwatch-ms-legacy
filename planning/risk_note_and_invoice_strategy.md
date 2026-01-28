# Risk Note & Invoice System Refinement Strategy

## 1. Core Architecture: Decoupling Risk Notes from Invoices

### The Problem
Currently, every `RiskNote` is treated as an "Invoice" (Debit Note). In reality:
- **Risk Note:** A document summarizing a specific transaction (New Business, Renewal, Endorsement) and its coverage. It is an internal/underwriting document.
- **Invoice (Debit Note):** A billing request. A single invoice might bundle multiple Risk Notes (e.g., a fleet of 5 vehicles renewed together).

### The Solution: Introduce an `Invoice` Entity
We will decouple these by adding an `Invoice` model that acts as a collection of `RiskNotes`.

- **Invoice Model:**
    - `id`, `invoice_number`, `client_id`, `status` (Unpaid, Partial, Paid).
    - `line_items`: A relationship to one or more `RiskNotes`.
    - `total_amount`: Aggregated total of all linked Risk Notes.

## 2. Refined Document Templates

### Risk Note Template Refinement
Based on `Risk Note - sample.docx`, we will update `RiskNoteTemplate.tsx` to include:
- **Intermediary Details:** Clearly showing the agency branding vs the insurer.
- **Detailed Asset Tables:** E.g., for Motor, showing Chassis No, Engine No, Make/Model in a structured grid.
- **Scope of Cover:** A more professional "Schedule of Benefits" section.

### Invoice (Debit Note) Template
- Focus on the **Financial Summary**.
- Group by Policy Number if multiple policies are included.
- Explicit "Balance Due" and "Payment History" sections.

## 3. New Module: Payments & Invoicing (`/finance`)

### Financial Hub (Client Level)
Add a "Payments & Invoicing" view under the Client Hub.
- **Content:**
    - **Open Invoices:** Unpaid or partially paid bills.
    - **Payment History:** Receipts and allocations.
    - **Archival:** Links to uploaded images/PDFs of Cheques and Receipts.

## 4. Implementation Roadmap

### Phase 1: Risk Note Polish (UI)
- [x] Refactor `templates/RiskNoteTemplate.tsx` (Internal/Transaction View) to match professional standards.
- [x] Update `templates/Certificate.tsx` to handle more granular asset data (Chassis, Engine).

### Phase 2: Invoice Logic (Backend & Frontend)
- [ ] Implement `Invoice` model in the backend.
- [ ] Create a "Generation Engine" utility that can take N Risk Notes and produce 1 Invoice.

### Phase 3: Financial Management View
- [ ] Implement the `Financials` view in the frontend.
- [ ] Add `PaymentAllocation` UI to allow partial payments against specific invoices.
- [ ] Integrate `DocumentManager` for archival of Cheques/Receipts.

## 5. Workflow Refinement
1. **Underwriting:** Create/Renew Policy -> Generate **Risk Note**.
2. **Billing:** Select one or more Risk Notes -> Generate **Invoice (Debit Note)**.
3. **Cashiering:** Receive Payment -> Create **Receipt** -> Allocate to **Invoice**.
